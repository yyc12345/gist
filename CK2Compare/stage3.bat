@echo off

rem do generate
py FunctionGenerator.py "CK2Cmp.txt" "CK3.cpp" "CK2_ExportFunc.txt" "CK2_DemangledExportFunc.txt"
py FunctionGenerator.py "VxMathCmp.txt" "VyMath.cpp" "VxMath_ExportFunc.txt" "VxMath_DemangledExportFunc.txt"