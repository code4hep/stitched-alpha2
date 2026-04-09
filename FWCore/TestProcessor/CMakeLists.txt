# FWCore/TestProcessor library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_TestProcessor SHARED ${SOURCES})
add_library(Stitched::FWCore_TestProcessor ALIAS stitched_FWCore_TestProcessor)

target_include_directories(stitched_FWCore_TestProcessor
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_TestProcessor
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_TestProcessor
    PUBLIC
        Stitched::DataFormats_Common
        Stitched::DataFormats_Provenance
        Stitched::FWCore_Concurrency
        Stitched::FWCore_Framework
        Stitched::FWCore_PythonParameterSet
        Stitched::FWCore_ServiceRegistry
        Stitched::FWCore_Utilities
    PRIVATE
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_ParameterSetReader
        Stitched::FWCore_PluginManager
)

set_target_properties(stitched_FWCore_TestProcessor PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_TestProcessor
)

stitched_install_python()
