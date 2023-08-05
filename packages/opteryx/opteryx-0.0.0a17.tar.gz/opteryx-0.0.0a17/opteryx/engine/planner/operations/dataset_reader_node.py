"""
Dataset Reader Node

This is a SQL Query Execution Plan Node.

This Node reads and parses the data from a dataset into a Table.

We plan to do the following:

USE THE ZONEMAP:
- Respond to simple aggregations using the zonemap, such as COUNT(*)
- Use BRIN and selections to filter out blobs from being read that don't contain
  records which can match the selections.

PARALLELIZE READING:
- As one blob is read, the next is immediately cached for reading
"""
import time
from enum import Enum
from typing import Iterable
from opteryx.engine.planner.operations import BasePlanNode
from opteryx.engine import QueryStatistics
from opteryx.storage import file_decoders
from opteryx.storage.adapters import DiskStorage
from opteryx.storage.schemes import MabelPartitionScheme


class EXTENSION_TYPE(str, Enum):
    # labels for the file extentions
    DATA = "DATA"
    CONTROL = "CONTROL"


do_nothing = lambda x: x

KNOWN_EXTENSIONS = {
    "complete": (do_nothing, EXTENSION_TYPE.CONTROL),
    "ignore": (do_nothing, EXTENSION_TYPE.CONTROL),
    "metadata": (do_nothing, EXTENSION_TYPE.CONTROL),
    "arrow": (file_decoders.arrow_decoder, EXTENSION_TYPE.DATA),
    "jsonl": (file_decoders.jsonl_decoder, EXTENSION_TYPE.DATA),
    "orc": (file_decoders.orc_decoder, EXTENSION_TYPE.DATA),
    "parquet": (file_decoders.parquet_decoder, EXTENSION_TYPE.DATA),
    "zstd": (file_decoders.zstd_decoder, EXTENSION_TYPE.DATA),
}


class DatasetReaderNode(BasePlanNode):
    def __init__(self, statistics: QueryStatistics, **config):
        """
        The Dataset Reader Node is responsible for reading the relevant blobs
        and returning a Table/Relation.
        """
        self._dataset = config.get("dataset", "").replace(".", "/") + "/"
        self._reader = config.get("reader", DiskStorage())
        self._partition_scheme = config.get("partition_scheme", MabelPartitionScheme())

        self._statistics = statistics

        # pushed down projection
        self._projection = config.get("projection")
        # pushed down selection
        self._selection = config.get("selection")

    def __repr__(self):
        return self._dataset

    def execute(self, data_pages: Iterable) -> Iterable:

        if self._dataset.lower() == "$satellites/":
            from opteryx import samples

            yield samples.satellites()
            return
        if self._dataset.lower() == "$planets/":
            from opteryx import samples

            yield samples.planets()
            return

        partitions = self._reader.get_partitions(
            dataset=self._dataset,
            partitioning=self._partition_scheme.partition_format(),
        )

        self._statistics.partitions_found = len(partitions)

        for partition in partitions:

            self._statistics.partitions_scanned += 1

            # Get a list of all of the blobs in the partition.
            blob_list = self._reader.get_blob_list(partition)

            # remove folders, end with '/'
            blob_list = [blob for blob in blob_list if not blob.endswith("/")]

            # Track how many blobs we found
            self._statistics.count_blobs_found += len(blob_list)

            # Filter the blob list to just the frame we're interested in
            if self._partition_scheme is not None:
                blob_list = self._partition_scheme.filter_blobs(blob_list)

            # If there's a zonemap for the partition, read it
            #        zonemap = {}
            #        zonemap_files = [blob for blob in blob_list if blob.endswith("/frame.metadata")]
            #        if len(zonemap_files) == 1:
            #            # read the zone map into a dictionary
            #            try:
            #                import orjson
            #                zonemap = orjson.loads(self._reader.read_blob(zonemap_files[0]))
            #            except:
            #                pass

            if len(blob_list) > 0:
                self._statistics.partitions_read += 1

            for blob_name in blob_list:

                # the the blob filename extension
                extension = blob_name.split(".")[-1]

                # find out how to read this blob
                decoder, file_type = KNOWN_EXTENSIONS.get(extension, (None, None))
                # if it's not a known data file, skip reading it
                if file_type != EXTENSION_TYPE.DATA:
                    continue

                # can we eliminate this blob using the BRIN?
                #            pass

                # we're going to open this blob
                self._statistics.count_data_blobs_read += 1

                start_read = time.time_ns()

                # Read the blob from storage, it's just a stream of bytes at this point
                blob_bytes = self._reader.read_blob(blob_name)

                # record the number of bytes we're reading
                self._statistics.bytes_read_data += blob_bytes.getbuffer().nbytes

                # interpret the raw bytes into entries
                pyarrow_blob = decoder(blob_bytes, self._projection)

                self._statistics.time_data_read += time.time_ns() - start_read

                # we should know the number of entries
                self._statistics.rows_read += pyarrow_blob.num_rows
                self._statistics.bytes_processed_data += pyarrow_blob.nbytes

                # yield this blob
                print(f"reader yielding {blob_name} {pyarrow_blob.shape}")
                yield pyarrow_blob
