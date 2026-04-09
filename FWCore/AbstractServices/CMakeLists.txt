# FWCore/AbstractServices library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_AbstractServices SHARED ${SOURCES})
add_library(Stitched::FWCore_AbstractServices ALIAS stitched_FWCore_AbstractServices)

target_include_directories(stitched_FWCore_AbstractServices
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_AbstractServices
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

set_target_properties(stitched_FWCore_AbstractServices PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_AbstractServices
)
