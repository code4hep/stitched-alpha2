# FWCore/ParameterSet/bin - Build parameter set utilities

# edmPluginHelp executable
add_executable(edmPluginHelp edmPluginHelp.cpp)

target_include_directories(edmPluginHelp
    PRIVATE
        ${CMAKE_SOURCE_DIR}
)

target_link_libraries(edmPluginHelp
    PRIVATE
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Utilities
        Boost::program_options
)

# edmWriteConfigs executable
add_executable(edmWriteConfigs edmWriteConfigs.cpp)

target_include_directories(edmWriteConfigs
    PRIVATE
        ${CMAKE_SOURCE_DIR}
)

target_link_libraries(edmWriteConfigs
    PRIVATE
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Utilities
        Boost::program_options
)
