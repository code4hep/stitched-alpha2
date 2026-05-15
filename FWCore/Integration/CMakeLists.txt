# FWCore/Integration library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Integration SHARED ${SOURCES})

target_sources(stitched_FWCore_Integration
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Integration
    PUBLIC
        stitched_DataFormats_Common
        stitched_DataFormats_Provenance
        stitched_FWCore_Framework
        stitched_FWCore_ParameterSet
        stitched_FWCore_Utilities
        CLHEP::CLHEP
)

set_target_properties(stitched_FWCore_Integration PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_IntegrationPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                stitched_FWCore_Integration
                stitched_FWCore_Sources
                stitched_FWCore_Framework
                stitched_DataFormats_TestObjects
                stitched_DataFormats_Provenance
                stitched_FWCore_SharedMemory
                ROOT::Hist
                ROOT::Core
)
