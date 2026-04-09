# FWCore/PythonParameterSet library
file(GLOB SOURCES src/*.cc)

if(NOT SOURCES)
    message(FATAL_ERROR "No source files found for stitched_FWCore_PythonParameterSet")
endif()

add_library(stitched_FWCore_PythonParameterSet SHARED ${SOURCES})
add_library(Stitched::FWCore_PythonParameterSet ALIAS stitched_FWCore_PythonParameterSet)

#can't use target_sources as headers needed by other targets in this project
target_include_directories(stitched_FWCore_PythonParameterSet
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/interface>
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
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
