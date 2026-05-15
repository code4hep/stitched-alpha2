# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

stitched_generate_plugin(
    TARGET stitched_FWCore_ModulesPlugins
    SOURCES ${SOURCES}
    LINK_LIBRARIES
        stitched_FWCore_Sources
        stitched_FWCore_Framework
        stitched_FWCore_ParameterSet
)
