@echo off
set UNDNAME="E:\\VS2019\\VC\\Tools\\MSVC\\14.23.28105\\bin\\Hostx86\\x86\\undname.exe"

rem run strip
py FunctionStrip.py "ck2.txt" "CK2Test.txt"
py FunctionStrip.py "vxmath.txt" "VxMathTest.txt"

rem demangle it
%UNDNAME% "CK2Test.txt" > "CK2TestDemangled.txt"
%UNDNAME% "VxMathTest.txt" > "VxMathTestDemangled.txt"

rem run compare
py FunctionCompare.py

echo "Stage 2: please check CK2Cmp.txt and VxMathCmp.txt. Then fill then with correct value"