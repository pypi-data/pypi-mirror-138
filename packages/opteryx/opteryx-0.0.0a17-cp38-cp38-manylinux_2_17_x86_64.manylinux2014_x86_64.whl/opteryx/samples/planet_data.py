"""
planets
---------

This is a sample dataset build into the engine, this simplifies a few things:

- We can write test scripts using this data, knowing that it will always be available. 
- We can write examples using this data, knowing the results will always match.

This data was obtained from:
https://github.com/devstronomy/nasa-data-scraper/blob/master/data/json/planets.json

Licence @ 02-JAN-2022 when copied - MIT Licences attested, but data appears to be
from NASA, which is Public Domain.

To access this dataset you can either run a query against dataset :planets: or you
can instantiate a PlanetData() class and use it like a Relation.

This has a companion dataset, $satellites, to help test joins.
"""

if __name__ == "__main__":
    import sys
    import os

    sys.path.insert(1, os.path.join(sys.path[0], "../.."))

import io
import base64
import pyarrow.parquet as pq  # type:ignore


class PlanetData:
    @staticmethod
    def get():

        return pq.read_table(
            io.BytesIO(
                base64.b85decode(
                    b"P(e~L6$BNK0Tob86%rK$5&!@wwJ-f3Nc{i+zySaP00RI700jUB00#gF00{s90000000>k900RLP02Lq=GAtDm6$BLq6$Ts_2nhfH0000002l}X000000000M04N9v000000000O2mt^90000000000D77#BAP|8700IC201^QN1rRb+b_f6f04AaW92Eo^H3R?#85ja-WEBh+5*Ek;7McPkb|wfM7zhaf00000000;W0RR9100000762#+2><{9000007zhCX000000000PEENP51Qh}R6#x|k6#@VN02KrkumKgS0ZbJV6$BCh04TLD{UBIn0su0_5Ey{PEe60M>$~hy2qbo7@W~i7L34^|5h()QfbpBdRdvOpCGsE4RXhHZrvSCYk5*dxg+<eb->k(;ely5b^3sn20RV##R1_5e6(AKdEEN(J1QiAq1{^j3C<Rt!Zgq1Q1w~<UbZ7to04TLD{U8v500062000sJ1O*T>RCWje001VO1{@U(88rj|1{oLxZeeX@6$};<7PbNw!U86w1t!`995w(b1y*Hlb#oX6MPYJuXaE^36$BLo6#@Vi02Krk0ssI26$BNK0Tq@3OcfFp1QGxMD77#BAV?Jg0E7b{h3iqc9@Rg46s||%dJ{n5dK9il;TJ$927#4Bi{w85sGUFnz=1$BvsFL<fLTDFJS^0j=8ZoD6aWE)kURku02Lq=GAtDm6$BLq6$Ts_2mk;8005|+Ko|(0JS^0j=8ZoV04N9m00000sGUF<2%kJG)SBjvKL7v#D77#BAP|8700IC201^QN1rRb+b_f6f049nG92E)~H3R?#85jg@VRLg83>Fd=$^sVR0w&%FCa4D-7zh9W0001}oj@1}pFAwon&yo^762#+000000H~cn7zm#{EYzCjjXwYxEENP51Qh}R6#x|k6#@VN02KrkkO38bOcfFp1QGxMD77#BAV{?V05k#s0000053@i3q{l!2>c~I<h`K;@0YQLm{XoF==m0N-qCf}$ATj6xmViZ81cM+TNC1u%02Lq=GAtDm6$BLq6$Ts_2mk;806=sBK^O=C00000grYze04N9m0000$bOAva2mk;8004xdKmY&$D77#BAP|8700IC201^QN1rRb+b_f6f049<S92E)~H3R?#85js;X<=<;bY*fC3>Fd=$O0C~0w(4RCdvyO7zh9W002OA0YMlD000000ED7I762#+00000Ky(2?7zh9W0001lqCfx{EENP51Qh}R6#x|k6#@VN02KrkkO38LOcfFp1QGxMD77#BAV_rq0N4Nk0000pwLk!Sv_Jrgx~{mCc!k`Pn3-OnKnMU}U@$Nk7z_*s&P)a@Ti^&402Lq=GAtDm6$BLq6$Ts_2mk;8004@$Ko|%B00000c!fX~04N9m00000inTx(2mk;8004M}KmY&$D77#BAP|8700IC201^QN1rRb+b_f6f049<W92E)~H3R?#85jp-Wo~n6ba@pF77`Z70v5OeCgu<(+7BEU2mk;8004@$Ko|%B00000c!fX~04N9m00000inTx(2mk;8004M}KmZvm6$BLo6#@Vi02Krk0ssI26$BN40Tpgc6%Z8!5&!@wwJ-f3Ky?8C@S2&KnVFdlK+Vj|%*@OoKqDD9KmZ~@W+6ZTCgwi|05em7Hh>J=rIm5bFqaho6&w{VEEN(J1QiAq1{@d&nwgoInHe`g7zk!&W@ct)=06qyC<vOFnVFdxH$WH&W@ct)W@hF;0000ewJ-f34sieg0ssI25&;7Rh%nX%001V87914{88rj|1{oL!XL4b7X>@rN3>Fd=v;r2i0w&}XCfE}k7zmn~nVFdxH$WH&W@ct)W@hF;762#+nwgoInHe`g7zk!&W@ct)=05-#EENP51Qh}R6#x|k6#@VN02KrkkO38ROcfFp1QGxMD77#BAV`e?0QfUAGcz+Y5kSq%%*@QpBtT{+KmZiLO+idGfH%zaKL-F{;F$xL8VuyNG6LM#f+ZCI6(AKdEEN(J1QiAq1{@d&000000KiQ^7zoYG%*@Qp^gk8=C<p)m0002MO+Xk3&CJZq%*^yZ0000ewJ-f35P<*y0ssI25&;AS5HeJD2mk;8CXgB&6$%+O1ONsZ7!GA~V_|S*R%L8&V`+4G6$};<7RUk?z5*uX7$(ve92f`y00000z)e6H2+hpQ%*@R6KNbKe2mk;8006*EKo|(k%*@Qp%=AA187vh96$BLm02Kfg1Qh}R000#P6_5cHmH|u^5)}jz001bpFa01$6#@WM17>DsW@i4CKmY&$0D#E0z-Hz*K$@AEnVFe5K+Vj|%*@OqKxQRCGcmv!FhH7_nVFd>W55IeLkR{qfM!>)1Qh@kAQdt!6%rK$6$TXs92f{@W@ct){*^!&2mk;80D#E0z!m@~2xewxW@i4CKo|%B0001h$hN=$001bpFa018fdBvk0000I0R#mQGE{a50000c#vU9M3K=y700tQt4svgFVRUJ4Zct@%X>Vi|3>Fd=$^sVR0w$UrCgd9&7zk!&W@cvol|UE>00000fXKGM762#+W@ct)X8x5x7zh9W004l<w!i=xEENP51Qh}R6#x|k6#@VN02KrkkO38r0ZbJV6$BCh04TLD{UAv70RRL8nwgoInSQW90OX}W060K1Gcz+Yvp7J_%p*W%B{MNVnwgoInHexZnwgoInJHsH1pqrofE&OPXtIJM6#x|=6*4Rp5)}j$1{DSz7zmn~nVFe>us|3H&CJZq%*-P|762#+nwgoInSQW97zoYG%*@QpBR~KE04TLD{U8v500062000sJ1O*T>RCWje001WRA{-S888rj|1{oL&Y-Mg|bZAdzL}7Uq3>Fd=$^sVJ0w%~ICYm4|7zmn~nVFe>us|3H&CJZq%*-P|762#+nwgoInSQW97zoYG%*@QpBR~KdEENP51Qh}R6#x|k6#@VN02KrkkO38t0ZbJV6$BCh04TLD{UAvF0RSWeGcz+YGxJP9&CJZq%nVyVGqYlRY*dIq000000A`kPra+pRnVA`nu|Q^KW@cs*w?G5{V4#(OXAT~KB^3Y_AQdt!6%rK$6$TXs92f{@W@ct)61PAY2s1M?Gc)r{Ko$Tf2xewxW@Zw%Ko|%!Gcz+Y^GrYh001bpFa018fdBvk0000I0R#mQGE{a50000co+lg?3K=y700tQt4`gX`bYX5|WkzyuZBun_6$};<7Rmw^+yW-@B__fo92f{@W@ct)61PAY2s1M?Gc)r{Ko$Tf2xewxW@Zw%Ko|%!Gcz+Y^GrYh87vh96$BLm02Kfg1Qh}R000#P6_5cHkO52;5)}jz001bpFa01${Q&^<0ssI20000-Kmg!cKr>@vKr_>6Kma6%KxQJ9K$@AEnVD*(fLyUa&CJZq%v7;J1^_z+fgm6V2m*ox;0P4}6(AKdEEN(J1QiAq1{@d&00000fLyUa7zh9W00000M?e+;C<p)m004kou|OCI00000002io0000ewJ-f35P<*y0ssI25&;AS5HeJD2mk;8CeSM!6$%+O1ONsZ7z%J@a%pH~Y-w+96$};<7Rmw^+yW+~Dkk(O92f`y0001hT(LkH2mk;80000-Ko$Tf2mk;80DxSvKo|%B0000007pOo87vh96$BLm02Kfg1Qh}R000#P6_5cHkO52;5)}jz001bpFa01${Q&^v0y8r+Gc$8hK$@AEnVC6TKr;hlKxQUyK+Vj|%*=#|Kme+jKr?rzv%#_E&%8he087bOISh;dOTb7AECCe&6(AKdEEN(J1QiAq1{@d&W@ct)=Fhx97zi^nGcz-DQ9u>|C<ta|W@hHkyg(QTGcz+YGjmZu0000ewJ-f35P<*y0ssI25&;AS5HeJD2mk;8CipKL6$%+O1ONsZ7zkl-Xk~0^Z*CO~77`Z90v6l?Cd@7-oGly}2xewxX6DblKo|%!Gcz+Yb5TGR04NA%W@cvQ&%8hw2s1M?Gc$8hKmZvm6$BLo6#@Vi02Krk0ssI26$BNK0Tq5s6%rK$5&!@wwJ-f3NVNd~Gy(ts00000RzPMJY(O*9c0d4lg+Ku7uz>x<K;PW}GwmGqKnMU}2Dky*SP=|@fFK}90FD&^6(AKdEEN(J1QiAq1{@d&00000037x}7zh9W00000RzMa2C<p)m0000S_COd2000000034%0000ewJ-f35P<*y0ssI25&;AS5HeJD2mk;8CWtf~6$%+O1ONsZ7!7Z7Vrg_?Y*1x#X>Vi|3>Fd=$O0C~0w&xtCcrTq7zh9W0000S_COd2000000034%762#+00000037x}7zh9W00000RzLt5EENP51Qh}R6#x|k6#@VN02KrkkO38n0ZbJV6$BCh04TLD{UAu?0RYqjGcz+YGqXoP0DwV2&CJZq%*;JNnwgoInHe}hGb%u4BO93&K+Vj|%*@OZKm`Cp4Vjr2v;hbUz!4Py6(AKdEEN(J1QiAq1{@d&Gcz+YGqXoP7zoYG%*@Qp5<nIJC<rq%Gcz-@M?e?|&CJZq%*+x%0000ewJ-f35P<*y0ssI25&;AS5HeJD2mk;8Ca^dh6$%+O1ONsZ7!Pl9Vrg_?Y*uA#Z)0h6c@+#65*Eq=7S;kLgf}MIH5?cSGcz+YGqXoP7zoYG%*@Qp5<nIJC<rq%Gcz-@M?e?|&CJZq%*+x%02wS51Qi4o0ss{N6$BLm0000L1Qn106?{w;5)}jz001bpFa01$tpNZu0ssI20000SKr;(K0A~I_&CK*a00cmqnd$sLGcz+YGcz$j2LL-$03)CWSOmlcIa+W86#x|=6*4Rp5)}j$1{DSz7zi^nGcz+YF+dmy000000001h762#+Gcz+YGcz$j7zh9W000000Du4h04TLD{U8v500062000sJ1O*T>RCWje001V;JRB7Y88rj|1{oL<Z*pR3bYW~sZewg|Zeet3Z*CO~77`Z70v5&sCZIbehB_P=2s1M?Gcz+WKo|%B00000004j%04NAEGcz+YGciCI2mk;800000fB+dR6$BLo6#@Vi02Krk0ssI26$BNK0TrSFOcfFp1QGxMD77#BAV@(106hxVqi{XSKY8gUF$k=DKb*uMuySaTKdSN4O=1wZKS~S&D~A@TKgo8!pBgW%KU!ov-%pLFKe|Z_0xO4xKM1TGT4X!VKNSEKAQdt!6%rK$6$TXs92f`)tQ=ZoJI_BD2zluyF$k=DKNbKe2nehkT4X!VKNtvk=_WA<tb9KJ001bpFa018fdBvk0000I0R#mQGE{a50000cmO&g93K=y700tQt6K`^2X>?(1MPp-SZgg^KV`+4G6$};<7Rmw^?gA$2KPIR?92f`)tQ=ZoJI_BD2zluyF$k=DKNbKe2nehkT4X!VKNtvk=_WA<tb9KJ87vh96$BLm02Kfg1Qh}R000#P6_5cHgaJ$y5)}jz001bpFa01$%>e*}0-VGkuySajKh4a{%*-riKxQ{UGdV!b%m}kOb689~KmY&$005v~Kn4Ii2VNOCa~OyWZfwC46#x|=6*4Rp5)}j$1{DSz7zoYG%*@OzW<VGSoWvloa%iDH762#+&CJZq%q(U=7zmuiAh2?1p+5is04TLD{U8v500062000sJ1O*T>RCWje001V$MI03h88rj|1{oL-Z(?j|adl~Qc~oyta$;$86$};<7Rmw^&;llyL?-k?92f}A%*@QpEM`C$2%N+quySajKNbKe2+hpQ%*-riKo|&|#2~P8XrVs<87vh96$BLm02Kfg1Qh}R000#P6_5cHXiOCn6$BCh04TLD{UAtP0RX@N00000;AB7meJ(&yz<^s}U}ykoAZ)-00AOG+5DW&gf#v{~mAoxD0u=xiAQdt!6%rK$6$TXs92f`y000000DV9h2mk;8001Ctz!m@~2mk;80001eKo|%B00000AZ)+@001bpFa018fdBvk0000I0R#mQGE{a50000c&Pf~<3K=y700tQt4{c>(Zd7G$aAk5~bairN6$};<7RUk?vH~WeNG6;|92f`y000000DV9h2mk;8001Ctz!m@~2mk;80001eKo|%B00000AZ)+@87vh96$BLm02Kfg1Qh}R000#P6;KsWOce?h1QGxMD77#BASnF+0Js1ES3m&pKYJ9eN8x&eKk;beh_(3SJ^}zh7#zR?6#x|&6)G$h5)}j$1{DSz7zh9W00000S3npD000000001h76>Q^000000037&7zh9W000000Du4h04TLD{U8is00093000FK0RsbwMgS(XO&k>p88rj|1{oL+b9HiNVPj=ba%FRKb#i4D3>Fd={s9({0w$15CZtOo7zh9W00000S3npD000000001h76>Q^000000037&7zh9W000000Du4)EENP51Qh}R6#x|k6#@VN02KrkfB_XuOcf9n1QGxMD77#BAVBQ^0I&c60RRF3PXImu8vqUf1poj5000002UG$80|6BP6&w{VEEN(J1QiAq1{@d&PXGV_000007zh9W00000000&MC<spg00000000;W00000000000000ewJ-f34sieg0ssI25&;7RKs43|001VOQ5+Qn88rj|1{oL)Zgp*9WpYnuO>b{*a}^905*D-q7Lo!c^iL*=PaGHsPXGV_000007zh9W00000000&MC<spg00000000;W000000000002wS51Qi4o0ss{N6$BLm0000L0vY@jH2@d}b7N>_ZDAEC02Kr!0vG~mWB?TmB?1@(ZeeX@B>+qu0000L3MB#<1Z`n+a{v_zB?1@-WNBe-Wprh702K-)0vHEmWo~n6ba?<33MB#<2WN6&c4>5Z02K-)0vHZub7Ns}WmaWuZ)0h6c>om(B?1@@a&L5DbZKvHP-SvyZ)5-!3MB#<3v6X>XLM*!W<+6m02K-)0vHcuX>)X8ZewLea&K)@b#4F^3MB#<3UFm|X=r6^X>V=-6$&K+7zkl-Xk~0^Z*Bk;3MB#<4R3N{X>?(1P-SvyZ)5-!3MB#<4{vf}X>?(1R%L8&V`+4G02K-)0vHl+a$;$8VQfimV{B<|VRUJ4ZU7YuB?1@|Z*pR3bYW~oV`F7*baH89X>@r26$&K+7!Yq_Y-w?IX>@s1Z%=Y!X><S;3MB#<4{c>(Zd7G$aAk5~bairN02K-)0vHc-b#i85V`WfsWpi_Na%BJ&1SJ9(4Q_R9Vr6nqW=(HzZgT(@5*ZvB{1hgl0vr_t88rj|1{oLvX=D`)77`Z70v4JACUzzW92f`*000000000O2mt^90000002Tl!2nhfH0000002l}X000000000087vh96$BLm02Kfg1Qh}R001VO1{@U(88rj|1{oLxZeeX@6$};<7PbNw!U86w1t!`995w(b1y*Hlb#oX6MPYJuXaE^36$BLo6#@Vi02Krk0ssI2CW;Ci6$%+O1ONsZ7zAx$b8{6877`Z90v6%|Cf*1ps0SPv2mk;8005|+Ko|(0JS^0j=8ZoV04N9m00000sGUF<2%kJG)SBjvKL8ml6$BLo6#@Vi02Krk0ssI2CXx;u6$%+O1ONsZ7zku(VQpn}WpWh^77`Z70v5;uCguz#$_pGA2mk;806=sBK^O=C00000grYze04N9m0000$bOAva2mk;8004xdKmZvm6$BLo6#@Vi02Krk0ssI2CXx~y6$%+O1ONsZ7zbo!ZgXjLc@+#65*Ek;7PtZ?<`5>@4;&Z>000000E)Fh7zh9W0001Zg+LYnC<p)m0001rwLlmM000000C<H!02wS51Qi4o0ss{N6$BLm0000cj20Xf3K=y700tQt2WN6&c4>5Z6$};<7PJBuv;rpN6eidc92f|inVFfH88<)}2xewxW@cvQKNbKe2%4FhnVA_kKo|&SW@ct)X68Qt87vh96$BLm02Kfg1Qh}R001VC8XOf088rj|1{oL*WpiU;aAj6yY;R*}ba@pF77`Z70v5gkCgd0<(ia>U2mk;8006*EKo|(k%*@Qp%=AAN04N9m00000z)e6H2+hpQ%*@R6KL8ml6$BLo6#@Vi02Krk0ssI2CdM8d6$%+O1ONsZ7!Go8bYXO9Z*EX!a%pd56$};<7Rmw^;sPd`9VX-(92f{@W@ct){*^!&2mk;80D#E0z!m@~2xewxW@i4CKo|%B0001h$hN=$87vh96$BLm02Kfg1Qh}R001WRA{-S888rj|1{oL&Y-Mg|bZAdzL}7Uq3>Fd=$^sVJ0w%~ICYm4|7zmn~nVFe>us|3H&CJZq%*-P|762#+nwgoInSQW97zoYG%*@QpBR~KdEENP51Qh}R6#x|k6#@VN04AO%92E)~H3R?#85j>_X>)X8ZewLea&K)@b#4_577`Z90v6l?Ch{dF!Xz9R2xewxW@Zw%Ko|%!Gcz+Y^GrY%04NA%W@ct)61PAY2s1M?Gc)r{KmZvm6$BLo6#@Vi02Krk0ssI2CeSM!6$%+O1ONsZ7z%J@a%pH~Y-w+96$};<7Rmw^+yW+~Dkk(O92f`y0001hT(LkH2mk;80000-Ko$Tf2mk;80DxSvKo|%B0000007pOo87vh96$BLm02Kfg1Qh}R001WVFB}yL88rj|1{oL#VQ^?=Y-w+96$};<7Rmw^+yW-dE+(8U92f{@W@cvQ&%8hw2s1M?Gc$8hKo$Tf2xewxX6DblKo|%!Gcz+Yb5TG587vh96$BLm02Kfg1Qh}R001V4G#nKQ88rj|1{oL)Z*pR3bYW~zWpZh6WEBh+5*Ek;7RUl7+%hJ>F&r2O00000037x}7zh9W00000RzMa2C<p)m0000S_COd2000000034%02wS51Qi4o0ss{N6$BLm0000cus9qQ3K=y700tQt4{vf}X>?(1R%L8&V`+4G6$};<7Rmw^)&eGkHzwLO92f{QGcz+YvqwM}2+hpQ%*@OZKo$Tf2s1M?Gc&VCKo|(k%*@Qp%o0EV87vh96$BLm02Kfg1Qh}R001V;JRB7Y88rj|1{oL<Z*pR3bYW~sZewg|Zeet3Z*CO~77`Z70v5&sCZIbehB_P=2s1M?Gcz+WKo|%B00000004j%04NAEGcz+YGciCI2mk;800000fB+dR6$BLo6#@Vi02Krk0ssI2CYC`Q6$%+O1ONsZ7!z-DVrg_?Y(-;ZWo~qGX=7=0c@+#65*Eq=7VZKj>OUr^J{%Yb2&^1hWINA47zlakCNT)Cd_NWdC<q9w99m>M&p#LldFduG2&{ZR02wS51Qi4o0ss{N6$BLm0000c#6=tx3K=y700tQt5N~2^X>oOFba_;7PjX^ubQKI15*Eq=7SIAFm_#P@LL3+f&CJZq%q(U=7zmuiAh2?1p+6P?C<x8W%*@OzW<VGSoWvloa%iDH02wS51Qi4o0ss{N6$BLm0000c&Pf~<3K=y700tQt4{c>(Zd7G$aAk5~bairN6$};<7RUk?vH~WeNG6;|92f`y000000DV9h2mk;8001Ctz!m@~2mk;80001eKo|%B00000AZ)+@87vh96$BLm02Kfg1Qh}R001VmO&k>p88rj|1{oL+b9HiNVPj=ba%FRKb#i4D3>Fd={s9({0w$15CZtOo7zh9W00000S3npD000000001h76>Q^000000037&7zh9W000000Du4)EENP51Qh}R6#x|k6#@VN04AJK92Eo^H3R?#85j+2b!}p0a!+PWZ*OjM6$};<7PJBuk^(05PbP{_92f{s000000000O2mk;80000002Tl!2u}b20000002l}W000000000087vh96$BLm02Kfg1Qh}R000)QG8Pgh2p0A-6aWAj92g8iQc_P>I&))aWo=;?m<%s3FE1}NXGK9lK~X_LK|w)5K}$hFcR@mDK}JDAXF)?}K|w)5K|(@7K}|tHK|w=7K}kVDK|w-6K}kVDK|w-6K|w)6Q9(gLL1#iiK|wS@O+i6RcSJ!!LNq~lK|xbNO+i6IXGB3kL}x)~K|ygrNkKtKQA0sNK{!EYK|w=7NkKtQQ9?mMLt{ZvK|xwUML|JBXF@?iL~}twK|ymtK|w)CXF)+hLP0@6K|w-6K|w)9L^v-mI6*-{MMFhFK|w)7K|w)5K}A79K|w)5K|w)5FhM~<LUm+UF=<*@N>EyBF?M1yHF`loK|xSZdM__`K|w)5MnOSAK|y6udM__`K|w)LO;JHXK|x7DK|w)5Q9(gLK|w)5K|w@!K|w)CPBCL`T4-4^R#9VZR(fMIR(V=cL}f2fFE2qsK|?`HdN?mHI6*-{MMOnGK|w)7K|w)5K}A79K|w)5K|w)5I6*-{LUdYJMs-$4R&--WR(V-iQZZv~RY65|GcPZ9K|w)hL}xEhFE2qsK|(=zK|w)5L2E%lK|w-6K|w)5K|w)5K~X_LK|x|NN^@aYMloSnQZ-gbIZ$J5N^oRBK|w)5LQ5}ZFE2qsK|?`8YB?`2I6*-{MMOnGK|w)7Q9(gLK}A79K|w)5K|w)6O+i6HLUv<qN^oRHMsreEPHI|LH85jsY-(XxQZ+$IOgS$vI6*-{NkLUmGcPZ9K|w)LO;JHXK|xAEK|w)5Q9(gLK|w)5K|w`lK|w)BIeA%aY%p0@cuHbzPIF;bHE3i<Y<6O2K|ytPGcPZ9K|w)hLrE`YFE2qsK|(=zK|w)5L1#fhK|w-6K|w)5K|w)5K~O<KK|x|ON@-zOQfOjET5MuRIci~8QZ+$OH#sjaI6*-{NkMi{GcPZ9K|w)LO;JHXK|x7DK|w)5Q9(gLK|w)5K|w@OK|w)BIeA%aY%p0@cu`tdN^oK_Q9(gLL1`~`FE2qsK|?`ML^&@nI6*-{MMOnGK|w)6cR@ixK}A79K|w)5K|w)5XF)+hLTF=0Xl!CfY<6O2K|w)5LQ^kxFE2qsK|?`9L@O^ZI6*-{MMOnGK|w)6cR@ixK}A79K|w)5K|w)5Z$UvpLU&qNN^oIER&!xjIdwrnLqjiiFE2qsK|?`CL@O^ZI6*-{MMOnGK|w)7K|w)5K}A79K|w)5K|w)5I6*-{LTh1IPB2+lHELQ_T6tnJF;rw%G(mKBH!m-DK|w)hLq#ukFE2qsK|(=zK|w)5L1RHdK|w-6K|w)5K|w)5K}<nGK|x|iR&`o4Qg2i;T18n{Ye6-3H!m-DK|w)hLohFPFE2qsK|(=zK|w)5L1#fhK|w-6K|w)5K|w)5K~F(JK|y0}IWSpRQgC82HBnkvN^oK_Q9(gMaxX70I6*-{NkKMHH!m-DK|w)LO;JHXK|x7DK|w)5Q9(gLK|w)5K|w@kK|w)BR(e@7Mt53PT5MuRIci~8QZ+$ALQgL*FE2qsK|?`8dM__8I6*-{MMOnGK|w)6XF)+hK}A79K|w)5K|w)5V?jYdLT+PiMlxYoQZ+$HaxX70I6*-{NkLOkFE1~5K|w)LO;JHXK|x1BK|w)5Q9(gLK|w)5K|w-yK|w)BQfy*wPH<#MYe8^!FE1~5K|w)hLNG5cFE2qsK|(=zK|w)5L1RHdK|w-6K|w)5K|w)5K}kVDK|xwaY-nOvRxnyvNkKtDK|wKgFE1~5K|w)hLu)TDFE2qsK|(=zK|w)5L1RHdK|w-6K|w)5K|w)5K}A79K|x|yMtWm+K|w-iK}kVDSwTW)K|w)5K|w)hL{%>@FE2qsK|(@OK|w)5L1RHdK|w-6K|w)5K|w)5K}A79K|x||Ms!+HK|w)5K}A79Q9(jMK|w)6K|w}AK}kVDSwTW~K}|tHK|w`9K~X_LK|w)5K|(=jK|w)5L1RHdK|w-6K|w)5K|w)5K|?`7K|x_xQ9(gLXF)_kK}kVDV?jefK|w)5K|w)5MnOSAK|w)5K|w)5Jv{&zA8=uEadl;MEn{$SEn#wUZ+9SeWpZ<AZ*CwqE-)@J8T=F+000~S02}}S8~^|u000~S02}}S8~^|u000~S02}}S8~^|u000~S02}}S8~^|u000~S02}}S8~^|SArJrnP(e~L"
                )
            )
        )


if __name__ == "__main__":  # pragma: no cover

    md = PlanetData().get()

    print(md.schema)
    print(md.shape)
