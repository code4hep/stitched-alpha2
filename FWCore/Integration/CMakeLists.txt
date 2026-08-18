# FWCore/Integration library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Integration SHARED ${SOURCES})
add_library(Stitched::FWCore_Integration ALIAS stitched_FWCore_Integration)

target_include_directories(stitched_FWCore_Integration
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_Integration
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Integration
    PUBLIC
        Stitched::DataFormats_Common
        Stitched::DataFormats_Provenance
        Stitched::FWCore_Framework
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_Utilities
        CLHEP::CLHEP
)

set_target_properties(stitched_FWCore_Integration PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Integration
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_IntegrationPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                Stitched::FWCore_Integration
                Stitched::FWCore_Sources
                Stitched::FWCore_Framework
                Stitched::DataFormats_TestObjects
                Stitched::DataFormats_Provenance
                Stitched::FWCore_SharedMemory
                ROOT::Hist
                ROOT::Core
)
