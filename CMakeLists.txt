cmake_minimum_required(VERSION 3.23...4.0)

project(Stitched VERSION 1.0.0 LANGUAGES CXX)

# Set default build type if not specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Build type" FORCE)
endif()

# Set C++ standard (C++20 required for concepts)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules")

# Configure StitchedMacros.cmake for the build tree
# During build, edmWriteConfigs is in CMAKE_RUNTIME_OUTPUT_DIRECTORY
set(STITCHED_EXECUTABLES_DIR "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}")
set(STITCHED_INCLUDES_DIR ${CMAKE_SOURCE_DIR})
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules/StitchedMacros.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake-modules/StitchedMacros.cmake
    @ONLY
)

# Include Stitched utility macros (build tree version)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_BINARY_DIR}/cmake-modules")
include(StitchedMacros)

find_package(Boost REQUIRED COMPONENTS program_options)
message(STATUS "Found Boost: ${Boost_VERSION} at ${Boost_DIR}")
find_package(Threads REQUIRED)
find_package(TBB REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(tinyxml2 REQUIRED)
find_package(c4h_md5 REQUIRED)
find_package(CLHEP REQUIRED)
find_package(pybind11 REQUIRED)
find_package(CpuFeatures REQUIRED)
#the include derived from CpuFeatures appears to point to the wrong directory
get_target_property(CPU_INCLUDES CpuFeatures::cpu_features INTERFACE_INCLUDE_DIRECTORIES)
set_target_properties(CpuFeatures::cpu_features PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CPU_INCLUDES};${CPU_INCLUDES}/..")

# Find UUID
find_package(PkgConfig REQUIRED)
pkg_check_modules(UUID REQUIRED IMPORTED_TARGET uuid)

# Find ROOT
find_package(ROOT REQUIRED COMPONENTS Core RIO Net Hist Tree)
message(STATUS "Found ROOT: ${ROOT_VERSION} at ${ROOT_DIR}")

# Include GNUInstallDirs early so variables are available for environment scripts
include(GNUInstallDirs)


# Add compile options
add_compile_options(-Wall -Werror=return-type -Wno-attributes -DPROJECT_VERSION="1_0_0" -DCMS_MICRO_ARCH="UNKNOWN")
add_link_options(LINKER:-z,defs)

# Add subdirectories
add_subdirectory(DataFormats)
add_subdirectory(FWCore)

# Generate plugin cache for all plugin libraries
stitched_generate_plugincache(
    PLUGIN_TARGETS
        stitched_FWCore_ModulesPlugins
        stitched_FWCore_IntegrationPlugins
        stitched_FWCore_MessageServicePlugins
        stitched_FWCore_ServicesPlugins
        stitched_FWCore_TestModulesPlugins
)

# Configure environment setup scripts
include(ConfigureEnvironmentScripts)

# ============================================================================
# Installation and package configuration
# ============================================================================

include(CMakePackageConfigHelpers)

# Set installation directories
set(INCLUDE_INSTALL_DIR ${CMAKE_INSTALL_INCLUDEDIR})
set(LIB_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR})
set(BIN_INSTALL_DIR ${CMAKE_INSTALL_BINDIR})
set(CONFIG_INSTALL_DIR ${CMAKE_INSTALL_LIBDIR}/cmake/Stitched)

# Install all targets with EXPORT
# Note: This assumes all libraries are built as SHARED libraries
# and should be exported together

# Get all library targets that were created
set(Stitched_EXPORT_TARGETS
    # FWCore libraries
    stitched_FWCore_Utilities
    stitched_FWCore_PluginManager
    stitched_FWCore_Reflection
    stitched_FWCore_Version
    stitched_FWCore_ParameterSet
    stitched_FWCore_ParameterSetReader
    stitched_FWCore_PythonParameterSet
    stitched_FWCore_ServiceRegistry
    stitched_FWCore_MessageLogger
    stitched_FWCore_MessageService
    stitched_FWCore_AbstractServices
    stitched_FWCore_Concurrency
    stitched_FWCore_SharedMemory
    stitched_FWCore_Common
    stitched_FWCore_Framework
    stitched_FWCore_Sources
    stitched_FWCore_PythonFramework
    stitched_FWCore_TestProcessor
    stitched_FWCore_Services
    stitched_FWCore_Integration
    # DataFormats libraries
    stitched_DataFormats_Common
    stitched_DataFormats_Provenance
    stitched_DataFormats_TestObjects
    stitched_DataFormats_StdDictionaries_map
    stitched_DataFormats_StdDictionaries_others
    stitched_DataFormats_StdDictionaries_pair
    stitched_DataFormats_StdDictionaries_vector
    stitched_DataFormats_WrappedStdDictionaries
)

# Install libraries and executables
foreach(target ${Stitched_EXPORT_TARGETS})
    if(TARGET ${target})
        install(TARGETS ${target}
            EXPORT StitchedTargets
            LIBRARY DESTINATION ${LIB_INSTALL_DIR}
            ARCHIVE DESTINATION ${LIB_INSTALL_DIR}
            RUNTIME DESTINATION ${BIN_INSTALL_DIR}
            FILE_SET HEADERS
        )
    endif()
endforeach()

# Plugin libraries are dlopen-loaded at runtime via edmplugin::PluginManager /
# .edmplugincache and are never referenced via target_link_libraries by another
# CMake target, so they are not part of the Stitched:: export set. They are
# still built and installed as regular (non-exported) shared libraries; they
# have no public headers today, so a plain install(TARGETS) (no EXPORT, no
# FILE_SET) is sufficient.
set(Stitched_PLUGIN_TARGETS
    stitched_FWCore_ModulesPlugins
    stitched_FWCore_IntegrationPlugins
    stitched_FWCore_MessageServicePlugins
    stitched_FWCore_ServicesPlugins
    stitched_FWCore_TestModulesPlugins
)

foreach(target ${Stitched_PLUGIN_TARGETS})
    if(TARGET ${target})
        install(TARGETS ${target}
            LIBRARY DESTINATION ${LIB_INSTALL_DIR}
            ARCHIVE DESTINATION ${LIB_INSTALL_DIR}
            RUNTIME DESTINATION ${BIN_INSTALL_DIR}
        )
    endif()
endforeach()

# Install executables
set(Stitched_EXECUTABLES
    cmsRun
    edmPluginDump
    edmPluginHelp
    edmPluginRefresh
    edmWriteConfigs
)

foreach(exec ${Stitched_EXECUTABLES})
    if(TARGET ${exec})
        install(TARGETS ${exec}
            EXPORT StitchedTargets
            RUNTIME DESTINATION ${BIN_INSTALL_DIR}
        )
    endif()
endforeach()

# Note: Header files are now installed via target_sources FILE_SET in individual CMakeLists.txt files

# install python
# Note: DESTINATION must be relative to the install prefix (not the absolute
# ${CMAKE_INSTALL_PREFIX}) so that `cmake --install --prefix <dir>` overrides
# are honored correctly at install time.
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/python
        DESTINATION .)

# Export targets file
install(EXPORT StitchedTargets
    FILE StitchedTargets.cmake
    NAMESPACE Stitched::
    DESTINATION ${CONFIG_INSTALL_DIR}
)

# Configure StitchedMacros.cmake for the install tree
# When installed, edmWriteConfigs will be in ${CMAKE_INSTALL_PREFIX}/bin
set(STITCHED_EXECUTABLES_DIR "${CMAKE_INSTALL_PREFIX}/bin")
set(STITCHED_INCLUDES_DIR "${CMAKE_INSTALL_PREFIX}/include")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake-modules/StitchedMacros.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/cmake-modules-install/StitchedMacros.cmake
    @ONLY
)

# Configure and install package config files
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/StitchedConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfig.cmake
    INSTALL_DESTINATION ${CONFIG_INSTALL_DIR}
    PATH_VARS INCLUDE_INSTALL_DIR LIB_INSTALL_DIR
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/StitchedConfigVersion.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/cmake-modules-install/StitchedMacros.cmake
    DESTINATION ${CONFIG_INSTALL_DIR}
)

# Print installation information
message(STATUS "Stitched will be installed to: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  Libraries: ${CMAKE_INSTALL_PREFIX}/${LIB_INSTALL_DIR}")
message(STATUS "  Headers: ${CMAKE_INSTALL_PREFIX}/${INCLUDE_INSTALL_DIR}")
message(STATUS "  CMake config: ${CMAKE_INSTALL_PREFIX}/${CONFIG_INSTALL_DIR}")

