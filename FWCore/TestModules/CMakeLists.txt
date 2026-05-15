# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_TestModulesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
        stitched_FWCore_Framework
        stitched_DataFormats_Provenance
        stitched_FWCore_AbstractServices
        stitched_FWCore_PluginManager
        stitched_FWCore_Sources
        stitched_FWCore_ParameterSet
        stitched_FWCore_Utilities
)
