# FWCore/PluginManager/bin - Build plugin manager utilities

# edmPluginRefresh executable
add_executable(edmPluginRefresh refresh.cc)

target_include_directories(edmPluginRefresh
    PRIVATE
        ${CMAKE_SOURCE_DIR}
)

target_link_libraries(edmPluginRefresh
    PRIVATE
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Utilities
        Boost::program_options
)

# edmPluginDump executable
add_executable(edmPluginDump dump.cc)

target_include_directories(edmPluginDump
    PRIVATE
        ${CMAKE_SOURCE_DIR}
)

target_link_libraries(edmPluginDump
    PRIVATE
        Stitched::FWCore_PluginManager
        Boost::program_options
)
