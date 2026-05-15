# FWCore/Version library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Version SHARED ${SOURCES})

target_sources(stitched_FWCore_Version
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

set_target_properties(stitched_FWCore_Version PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
