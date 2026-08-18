# FWCore/Sources library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Sources SHARED ${SOURCES})
add_library(Stitched::FWCore_Sources ALIAS stitched_FWCore_Sources)

target_include_directories(stitched_FWCore_Sources
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_Sources
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Sources
    PUBLIC
        Stitched::FWCore_Framework
        Stitched::FWCore_Utilities
)

set_target_properties(stitched_FWCore_Sources PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Sources
)
