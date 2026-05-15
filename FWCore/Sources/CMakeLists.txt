# FWCore/Sources library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Sources SHARED ${SOURCES})

target_sources(stitched_FWCore_Sources
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Sources
    PUBLIC
        stitched_FWCore_Framework
        stitched_FWCore_Utilities
)

set_target_properties(stitched_FWCore_Sources PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
