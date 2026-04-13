# FWCore/Version library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreVersion SHARED ${SOURCES})

target_sources(FWCoreVersion
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

set_target_properties(FWCoreVersion PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
