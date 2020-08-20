@echo off
set DUMPBIN="E:\\VS2019\\VC\\Tools\\MSVC\\14.23.28105\\bin\\Hostx86\\x86\\dumpbin.exe"
set TARGETDLL="F:\\Ballance\\Ballance\\BuildingBlocks\\TT_Toolbox_RT.dll"

rem dump data
%DUMPBIN% %TARGETDLL% /IMPORTS:CK2.dll > ck2.txt
%DUMPBIN% %TARGETDLL% /IMPORTS:VxMath.dll > vxmath.txt

echo "Stage 1: please edit ck2.txt and vxmath.txt"