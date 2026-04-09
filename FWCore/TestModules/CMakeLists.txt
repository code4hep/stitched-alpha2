# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_TestModulesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
        Stitched::DataFormats_Common
        Stitched::DataFormats_Provenance
        Stitched::FWCore_AbstractServices
        Stitched::FWCore_Framework
        Stitched::FWCore_MessageLogger
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Sources
        Stitched::FWCore_Utilities
)
