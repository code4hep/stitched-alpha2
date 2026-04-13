# FWCore/ServiceRegistry library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreServiceRegistry SHARED ${SOURCES})

target_sources(FWCoreServiceRegistry
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(FWCoreServiceRegistry
    PUBLIC
        FWCoreAbstractServices
        DataFormatsProvenance
        FWCoreParameterSet
        FWCoreMessageLogger
        FWCorePluginManager
        FWCoreUtilities
        Boost::boost
        TBB::tbb
)

set_target_properties(FWCoreServiceRegistry PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
