# FWCore/Modules library
file(GLOB SOURCES plugins/*.cc)

stitched_generate_plugin(
    TARGET stitched_FWCore_ModulesPlugins
    SOURCES ${SOURCES}
    LINK_LIBRARIES
        Stitched::FWCore_Sources
        Stitched::FWCore_Framework
        Stitched::FWCore_ParameterSet
)
