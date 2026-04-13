# FWCore/Services library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreServices SHARED ${SOURCES})

target_sources(FWCoreServices
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreServices
    PUBLIC
        FWCoreAbstractServices
        FWCoreMessageLogger
        FWCoreParameterSet
        FWCoreServiceRegistry
        DataFormatsProvenance
        FWCoreUtilities
        Boost::boost
        CLHEP::CLHEP
        CpuFeatures::cpu_features
        ROOT::Tree
        ROOT::Hist
        atomic
)

set_target_properties(FWCoreServices PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET FWCoreServicesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                FWCoreServices
                FWCoreFramework
)
