# FWCore/ParameterSet/bin - Build parameter set utilities

# edmPluginHelp executable
add_executable(edmPluginHelp edmPluginHelp.cpp)

target_link_libraries(edmPluginHelp
    PRIVATE
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Utilities
        Boost::program_options
)

# edmWriteConfigs executable
add_executable(edmWriteConfigs edmWriteConfigs.cpp)

target_link_libraries(edmWriteConfigs
    PRIVATE
        Stitched::FWCore_ParameterSet
        Stitched::FWCore_PluginManager
        Stitched::FWCore_Utilities
        Boost::program_options
)
