# FWCore/MessageService library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreMessageService SHARED ${SOURCES})

target_sources(FWCoreMessageService
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreMessageService
    PUBLIC
        FWCoreMessageLogger
        FWCoreParameterSet
        FWCoreServiceRegistry
        FWCoreUtilities
        Threads::Threads
)

set_target_properties(FWCoreMessageService PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET FWCoreMessageServicePlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                FWCoreMessageService
                FWCoreFramework
)
