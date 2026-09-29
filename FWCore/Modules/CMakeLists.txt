# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

stitched_generate_plugin(
    TARGET stitched_FWCore_ModulesPlugins
    SOURCES ${SOURCES}
    LINK_LIBRARIES
        Stitched::DataFormats_Common
        Stitched::DataFormats_Provenance
        Stitched::FWCore_Framework
        Stitched::FWCore_MessageLogger
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_Reflection
        Stitched::FWCore_ServiceRegistry
        Stitched::FWCore_Sources
        Stitched::FWCore_Utilities
)
