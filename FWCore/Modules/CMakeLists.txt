# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

stitched_generate_plugin(
    TARGET FWCoreModulesPlugins
    SOURCES ${SOURCES}
    LINK_LIBRARIES
        FWCoreSources
        FWCoreFramework
        FWCoreParameterSet
)
