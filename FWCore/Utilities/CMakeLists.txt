# FWCore/Utilities library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h interface/*.icc)

add_library(stitched_FWCore_Utilities SHARED ${SOURCES})
add_library(Stitched::FWCore_Utilities ALIAS stitched_FWCore_Utilities)

target_include_directories(stitched_FWCore_Utilities
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_SOURCE_DIR}>
        $<INSTALL_INTERFACE:include>
)

# Associate headers with the target using FILE_SET
target_sources(stitched_FWCore_Utilities
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

target_link_libraries(stitched_FWCore_Utilities
    PUBLIC
        Boost::boost
        TBB::tbb
        Threads::Threads
        c4h_md5::c4h_md5
)

# Try to link UUID if available
find_library(UUID_LIBRARY uuid)
if(UUID_LIBRARY)
    target_link_libraries(stitched_FWCore_Utilities PUBLIC ${UUID_LIBRARY})
endif()

set_target_properties(stitched_FWCore_Utilities PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
    EXPORT_NAME FWCore_Utilities
)

stitched_install_python()
