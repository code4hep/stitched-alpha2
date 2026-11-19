# FWCore/PythonParameterSet library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

if(NOT SOURCES)
    message(FATAL_ERROR "No source files found for stitched_FWCore_PythonParameterSet")
endif()

add_library(stitched_FWCore_PythonParameterSet SHARED ${SOURCES})
add_library(Stitched::FWCore_PythonParameterSet ALIAS stitched_FWCore_PythonParameterSet)

target_sources(stitched_FWCore_PythonParameterSet
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_PythonParameterSet
    PUBLIC
        Stitched::DataFormats_Provenance
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_Utilities
        Python3::Python
        pybind11::pybind11
)

set_target_properties(stitched_FWCore_PythonParameterSet PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_PythonParameterSet
)

stitched_install_python()
