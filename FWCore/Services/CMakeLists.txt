# FWCore/Services library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Services SHARED ${SOURCES})
add_library(Stitched::FWCore_Services ALIAS stitched_FWCore_Services)

target_sources(stitched_FWCore_Services
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Services
    PUBLIC
        Stitched::FWCore_MessageLogger
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_ServiceRegistry
)

set_target_properties(stitched_FWCore_Services PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Services
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_ServicesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                Stitched::DataFormats_Provenance
                Stitched::FWCore_AbstractServices
                Stitched::FWCore_Framework
                Stitched::FWCore_Services
                Stitched::FWCore_Utilities
                Boost::boost
                CpuFeatures::cpu_features
                ROOT::Tree
                ROOT::Hist
                atomic
)
