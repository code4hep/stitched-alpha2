# FWCore/Integration library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreIntegration SHARED ${SOURCES})

target_sources(FWCoreIntegration
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreIntegration
    PUBLIC
        DataFormatsCommon
        DataFormatsProvenance
        FWCoreFramework
        FWCoreParameterSet
        FWCoreUtilities
        CLHEP::CLHEP
)

set_target_properties(FWCoreIntegration PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET FWCoreIntegrationPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                FWCoreIntegration
                FWCoreSources
                FWCoreFramework
                DataFormatsTestObjects
                DataFormatsProvenance
                FWCoreSharedMemory
                ROOT::Hist
                ROOT::Core
)
