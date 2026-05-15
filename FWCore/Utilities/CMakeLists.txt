# FWCore/Utilities library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h interface/*.icc)

add_library(stitched_FWCore_Utilities SHARED ${SOURCES})

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
)

# Copy and install Python files
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/python)
    file(RELATIVE_PATH PKG_PYTHON_PATH ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR})
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/python/
         DESTINATION ${CMAKE_BINARY_DIR}/python/${PKG_PYTHON_PATH}
         PATTERN "__pycache__" EXCLUDE
         PATTERN "*.pyc" EXCLUDE)
    install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/python/
            DESTINATION python/${PKG_PYTHON_PATH}
            PATTERN "__pycache__" EXCLUDE
            PATTERN "*.pyc" EXCLUDE)
endif()
