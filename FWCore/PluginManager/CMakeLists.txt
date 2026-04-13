# FWCore/PluginManager library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCorePluginManager SHARED ${SOURCES})

target_sources(FWCorePluginManager
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCorePluginManager
    PUBLIC
        FWCoreUtilities
        Boost::filesystem
        ${CMAKE_DL_LIBS}
        ROOT::Core
)

set_target_properties(FWCorePluginManager PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)

# Add bin directory for executables
add_subdirectory(bin)
