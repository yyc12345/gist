cmake_minimum_required(VERSION 3.23)
project(YYCFFT
    VERSION 1.0.0
    LANGUAGES CXX
)

option(YYCFFT_BUILD_TESTBENCH "Build testbench of YYCFFT." OFF)
include(GNUInstallDirs)

add_library(YYCFFT INTERFACE)
target_sources(YYCFFT
INTERFACE
FILE_SET HEADERS
FILES
    YYCFFT.hpp
)
install(TARGETS YYCFFT
    EXPORT YYCFFTTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILE_SET HEADERS DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

if (YYCFFT_BUILD_TESTBENCH)

    add_executable(YYCFFTTestbench "")
    target_sources(YYCFFTTestbench
    PRIVATE
        YYCFFTTestbench.cpp
    )
    target_include_directories(YYCFFTTestbench
    PRIVATE
        YYCFFT
    )
    target_link_libraries(YYCFFTTestbench
    PRIVATE
        YYCFFT
    )
    set_target_properties(YYCFFTTestbench
    PROPERTIES
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED 20
        CXX_EXTENSION OFF
    )
    target_compile_definitions(YYCFFTTestbench
    PRIVATE
        $<$<CXX_COMPILER_ID:MSVC>:UNICODE>
        $<$<CXX_COMPILER_ID:MSVC>:_UNICODE>
    )
    target_compile_options(YYCFFTTestbench
    PRIVATE
        $<$<CXX_COMPILER_ID:MSVC>:/utf-8>
    )

    install(TARGETS YYCFFTTestbench
        CONFIGURATIONS Release
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    )

endif ()
