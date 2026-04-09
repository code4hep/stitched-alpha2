# FWCore/Reflection library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_Reflection SHARED ${SOURCES})
add_library(Stitched::FWCore_Reflection ALIAS stitched_FWCore_Reflection)

target_include_directories(stitched_FWCore_Reflection
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_Reflection
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Reflection
    PUBLIC
        Stitched::FWCore_Utilities
        ROOT::Core
)

set_target_properties(stitched_FWCore_Reflection PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Reflection
)

stitched_install_python()
