# FWCore/Services library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Services SHARED ${SOURCES})

target_sources(stitched_FWCore_Services
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Services
    PUBLIC
        stitched_FWCore_AbstractServices
        stitched_FWCore_MessageLogger
        stitched_FWCore_ParameterSet
        stitched_FWCore_ServiceRegistry
        stitched_DataFormats_Provenance
        stitched_FWCore_Utilities
        Boost::boost
        CLHEP::CLHEP
        CpuFeatures::cpu_features
        ROOT::Tree
        ROOT::Hist
        atomic
)

set_target_properties(stitched_FWCore_Services PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_ServicesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                stitched_FWCore_Services
                stitched_FWCore_Framework
)
