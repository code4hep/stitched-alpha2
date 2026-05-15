# FWCore/MessageService library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_MessageService SHARED ${SOURCES})

target_sources(stitched_FWCore_MessageService
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_MessageService
    PUBLIC
        stitched_FWCore_MessageLogger
        stitched_FWCore_ParameterSet
        stitched_FWCore_ServiceRegistry
        stitched_FWCore_Utilities
        Threads::Threads
)

set_target_properties(stitched_FWCore_MessageService PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_MessageServicePlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                stitched_FWCore_MessageService
                stitched_FWCore_Framework
)
