@echo off
set DUMPBIN="E:\\VS2019\\VC\\Tools\\MSVC\\14.23.28105\\bin\\Hostx86\\x86\\dumpbin.exe"
set UNDNAME="E:\\VS2019\\VC\\Tools\\MSVC\\14.23.28105\\bin\\Hostx86\\x86\\undname.exe"
set TARGETDLL1="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_DatabaseManager_RT.dll"
set TARGETDLL2="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_Gravity_RT.dll"
set TARGETDLL3="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_InterfaceManager_RT.dll"
set TARGETDLL4="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_ParticleSystems_RT.dll"
set TARGETDLL5="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_Toolbox_RT.dll"

rem dump data
%DUMPBIN% %TARGETDLL1% /IMPORTS:CK2.dll > ck2_1.txt
%DUMPBIN% %TARGETDLL1% /IMPORTS:VxMath.dll > vxmath_1.txt
%DUMPBIN% %TARGETDLL2% /IMPORTS:CK2.dll > ck2_2.txt
%DUMPBIN% %TARGETDLL2% /IMPORTS:VxMath.dll > vxmath_2.txt
%DUMPBIN% %TARGETDLL3% /IMPORTS:CK2.dll > ck2_3.txt
%DUMPBIN% %TARGETDLL3% /IMPORTS:VxMath.dll > vxmath_3.txt
%DUMPBIN% %TARGETDLL4% /IMPORTS:CK2.dll > ck2_4.txt
%DUMPBIN% %TARGETDLL4% /IMPORTS:VxMath.dll > vxmath_4.txt
%DUMPBIN% %TARGETDLL5% /IMPORTS:CK2.dll > ck2_5.txt
%DUMPBIN% %TARGETDLL5% /IMPORTS:VxMath.dll > vxmath_5.txt

rem run strip
py FunctionStrip.py "ck2_1.txt" "ck2Test_1.txt"
py FunctionStrip.py "vxmath_1.txt" "vxmathTest_1.txt"
py FunctionStrip.py "ck2_2.txt" "ck2Test_2.txt"
py FunctionStrip.py "vxmath_2.txt" "vxmathTest_2.txt"
py FunctionStrip.py "ck2_3.txt" "ck2Test_3.txt"
py FunctionStrip.py "vxmath_3.txt" "vxmathTest_3.txt"
py FunctionStrip.py "ck2_4.txt" "ck2Test_4.txt"
py FunctionStrip.py "vxmath_4.txt" "vxmathTest_4.txt"
py FunctionStrip.py "ck2_5.txt" "ck2Test_5.txt"
py FunctionStrip.py "vxmath_5.txt" "vxmathTest_5.txt"

del ck2_1.txt
del ck2_2.txt
del ck2_3.txt
del ck2_4.txt
del ck2_5.txt
del vxmath_1.txt
del vxmath_2.txt
del vxmath_3.txt
del vxmath_4.txt
del vxmath_5.txt

rem demangle it
%UNDNAME% "ck2Test_1.txt" > "deck2_1.txt"
%UNDNAME% "vxmathTest_1.txt" > "devxmath_1.txt"
%UNDNAME% "ck2Test_2.txt" > "deck2_2.txt"
%UNDNAME% "vxmathTest_2.txt" > "devxmath_2.txt"
%UNDNAME% "ck2Test_3.txt" > "deck2_3.txt"
%UNDNAME% "vxmathTest_3.txt" > "devxmath_3.txt"
%UNDNAME% "ck2Test_4.txt" > "deck2_4.txt"
%UNDNAME% "vxmathTest_4.txt" > "devxmath_4.txt"
%UNDNAME% "ck2Test_5.txt" > "deck2_5.txt"
%UNDNAME% "vxmathTest_5.txt" > "devxmath_5.txt"

rem run compare
py FunctionCompare.py "result.txt" "5"

del ck2Test_1.txt
del ck2Test_2.txt
del ck2Test_3.txt
del ck2Test_4.txt
del ck2Test_5.txt
del vxmathTest_1.txt
del vxmathTest_2.txt
del vxmathTest_3.txt
del vxmathTest_4.txt
del vxmathTest_5.txt

del deck2_1.txt
del deck2_2.txt
del deck2_3.txt
del deck2_4.txt
del deck2_5.txt
del devxmath_1.txt
del devxmath_2.txt
del devxmath_3.txt
del devxmath_4.txt
del devxmath_5.txt

echo "Please edit result.txt"

