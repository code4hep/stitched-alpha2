# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_TestModulesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
        Stitched::FWCore_Framework
        Stitched::DataFormats_Provenance
        Stitched::FWCore_AbstractServices
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Sources
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_Utilities
)
