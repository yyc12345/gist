set DUMPBIN="E:\\VS2019\\VC\\Tools\\MSVC\\14.23.28105\\bin\\Hostx86\\x86\\dumpbin.exe"
set UNDNAME="E:\\VS2019\\VC\\Tools\\MSVC\\14.23.28105\\bin\\Hostx86\\x86\\undname.exe"
set TARGETDLL="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_Toolbox_RT.dll"

rem dump data
%DUMPBIN% %TARGETDLL% /IMPORTS:CK2.dll > ck2.txt
%DUMPBIN% %TARGETDLL% /IMPORTS:VxMath.dll > vxmath.txt

echo "please edit ck2.txt and vxmath.txt, then press any button"
pause

rem run strip
py FunctionStrip.py "ck2.txt" "CK2Test.txt"
py FunctionStrip.py "vxmath.txt" "VxMathTest.txt"

rem demangle it
%UNDNAME% "CK2Test.txt" > "CK2TestDemangled.txt"
%UNDNAME% "VxMathTest.txt" > "VxMathTestDemangled.txt"

rem run compare
py FunctionCompare.py
