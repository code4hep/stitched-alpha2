# FWCore/PythonFramework library
file(GLOB SOURCES src/*.cc)

if(NOT SOURCES)
    message(FATAL_ERROR "No source files found for stitched_FWCore_PythonFramework")
endif()

add_library(stitched_FWCore_PythonFramework SHARED ${SOURCES})
add_library(Stitched::FWCore_PythonFramework ALIAS stitched_FWCore_PythonFramework)

# The C++ header is private to the Python binding and intentionally not installed.
target_link_libraries(stitched_FWCore_PythonFramework
    PRIVATE
        Stitched::FWCore_Concurrency
        Stitched::FWCore_Framework
        Stitched::FWCore_MessageLogger
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_ServiceRegistry
        Stitched::FWCore_PythonParameterSet
        Stitched::FWCore_Utilities
        Python3::Python
        pybind11::pybind11
        TBB::tbb
)

set_target_properties(stitched_FWCore_PythonFramework PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_PythonFramework
)

stitched_install_python()
