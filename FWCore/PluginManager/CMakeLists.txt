# FWCore/PluginManager library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(stitched_FWCore_PluginManager SHARED ${SOURCES})

target_sources(stitched_FWCore_PluginManager
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_PluginManager
    PUBLIC
        stitched_FWCore_Utilities
        Boost::filesystem
        ${CMAKE_DL_LIBS}
        ROOT::Core
)

set_target_properties(stitched_FWCore_PluginManager PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

# Add bin directory for executables
add_subdirectory(bin)
