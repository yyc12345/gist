
# Check YYCC path environment variable
if (NOT DEFINED YYCC_PATH)
    message(FATAL_ERROR "You must set YYCC_PATH variable to one of YYCC CMake distribution installation path.")
endif()

# Find YYCC library
find_package(YYCCommonplace REQUIRED
    HINTS ${YYCC_PATH} NO_DEFAULT_PATH
)
