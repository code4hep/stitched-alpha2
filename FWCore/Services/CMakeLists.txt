# FWCore/Services library
file(GLOB PLUGIN_SOURCES plugins/*.cc)
stitched_generate_plugin(
    TARGET stitched_FWCore_ServicesPlugins
    SOURCES ${PLUGIN_SOURCES}
    LINK_LIBRARIES
                Stitched::DataFormats_Common
                Stitched::DataFormats_Provenance
                Stitched::FWCore_AbstractServices
                Stitched::FWCore_Concurrency
                Stitched::FWCore_Framework
                Stitched::FWCore_MessageLogger
                Stitched::FWCore_PluginManager
                Stitched::FWCore_Reflection
                Stitched::FWCore_ServiceRegistry
                Stitched::FWCore_Utilities
                Boost::boost
                CpuFeatures::cpu_features
                ROOT::Core
                ROOT::Hist
                ROOT::Tree
                TBB::tbb
                atomic
)
