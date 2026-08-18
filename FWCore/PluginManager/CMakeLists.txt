# FWCore/PluginManager library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_PluginManager SHARED ${SOURCES})
add_library(Stitched::FWCore_PluginManager ALIAS stitched_FWCore_PluginManager)

target_include_directories(stitched_FWCore_PluginManager
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

target_sources(stitched_FWCore_PluginManager
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_PluginManager
    PUBLIC
        Stitched::FWCore_Utilities
        ${CMAKE_DL_LIBS}
        ROOT::Core
)

set_target_properties(stitched_FWCore_PluginManager PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_PluginManager
)

# Add bin directory for executables
add_subdirectory(bin)
