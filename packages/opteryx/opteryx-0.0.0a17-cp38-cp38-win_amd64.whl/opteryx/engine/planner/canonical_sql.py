# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

"""
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], "../../.."))


def canonical_sql(ast, indent=False):

    statement = ""

    # SELECT
    statement += ast[0]["Query"]["body"]["Select"]["projection"]
    # FROM
    # WHERE
    # GROUP BY
    # HAVING
    # ORDER BY
    # LIMIT

    return statement
