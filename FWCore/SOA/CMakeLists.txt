# FWCore/SOA header-only library
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_SOA INTERFACE)
add_library(Stitched::FWCore_SOA ALIAS stitched_FWCore_SOA)

target_include_directories(stitched_FWCore_SOA
    INTERFACE
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_sources(stitched_FWCore_SOA
    INTERFACE
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

set_target_properties(stitched_FWCore_SOA PROPERTIES EXPORT_NAME FWCore_SOA)
