# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET FWCoreTestModulesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
        FWCoreFramework
        DataFormatsProvenance
        FWCoreAbstractServices
        FWCorePluginManager
        FWCoreSources
        FWCoreParameterSet
        FWCoreUtilities
)
