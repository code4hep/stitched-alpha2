# FWCore/Sources library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreSources SHARED ${SOURCES})

target_sources(FWCoreSources
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreSources
    PUBLIC
        FWCoreFramework
        FWCoreUtilities
)

set_target_properties(FWCoreSources PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
