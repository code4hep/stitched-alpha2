# FWCore/AbstractServices library
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS interface/*.h)

add_library(FWCoreAbstractServices SHARED ${SOURCES})

target_sources(FWCoreAbstractServices
    PUBLIC
        FILE_SET HEADERS
        BASE_DIRS ${CMAKE_SOURCE_DIR}
        FILES ${HEADERS}
)

set_target_properties(FWCoreAbstractServices PROPERTIES
    VERSION 1.0.0
    SOVERSION 1
)
