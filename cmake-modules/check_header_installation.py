#!/usr/bin/env python3
"""Install into a disposable staging area and test installed CMake targets."""

import argparse
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


EXCEPTION = Path("FWCore/PythonFramework/interface/PythonEventProcessor.h")

PROBES = {
    "reader": r'''#include "FWCore/ParameterSetReader/interface/ParameterSetReader.h"
#include "FWCore/ParameterSetReader/interface/ProcessDescImpl.h"
auto* volatile reader_symbol = &edm::getPSetFromConfig;
int main() { return reader_symbol == nullptr; }
''',
    "python_parameters": r'''#include "FWCore/PythonParameterSet/interface/MakePyBind11ParameterSets.h"
#include "FWCore/PythonParameterSet/interface/PyBind11ProcessDesc.h"
#include "FWCore/PythonParameterSet/interface/PyBind11Wrapper.h"
#include "FWCore/PythonParameterSet/interface/Python11ParameterSet.h"
auto* volatile python_symbol = &edm::cmspybind11::readPSetsFrom;
int main() { return python_symbol == nullptr; }
''',
    # Table.h currently relies on its includer to provide assert.
    "soa": r'''#include <cassert>
#include "FWCore/SOA/interface/Column.h"
#include "FWCore/SOA/interface/Table.h"
#include <array>
SOA_DECLARE_COLUMN(Count, int, "count");
SOA_DECLARE_COLUMN(Value, double, "value");
int main() {
  std::array<int, 1> counts{1};
  std::array<double, 1> values{2.0};
  edm::soa::Table<Count, Value> table(counts, values);
  return table.get<Count>(0) != 1 || table.get<Value>(0) != 2.0;
}
''',
    "test_objects": r'''#include <cassert>
#include "DataFormats/TestObjects/interface/TableTest.h"
int main() { edmtest::TableTest table; return table.size(); }
''',
}

CMAKE_PROJECT = r'''cmake_minimum_required(VERSION 3.23)
project(StitchedHeaderCheck LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Stitched CONFIG REQUIRED PATHS "${STAGED_CONFIG_DIR}" NO_DEFAULT_PATH)
file(REAL_PATH "${Stitched_CONFIG}" actual_config)
file(REAL_PATH "${STAGED_CONFIG_DIR}/StitchedConfig.cmake" expected_config)
if(NOT actual_config STREQUAL expected_config)
  message(FATAL_ERROR "Stitched config not from staged prefix: ${actual_config}")
endif()

if(NOT TARGET Stitched::FWCore_SOA)
  message(FATAL_ERROR "Missing Stitched::FWCore_SOA")
endif()
get_target_property(soa_imported Stitched::FWCore_SOA IMPORTED)
get_target_property(soa_type Stitched::FWCore_SOA TYPE)
if(NOT soa_imported OR NOT soa_type STREQUAL "INTERFACE_LIBRARY")
  message(FATAL_ERROR "Stitched::FWCore_SOA must be an imported INTERFACE library")
endif()
get_target_property(test_links Stitched::DataFormats_TestObjects INTERFACE_LINK_LIBRARIES)
if(NOT "Stitched::FWCore_SOA" IN_LIST test_links)
  message(FATAL_ERROR "Stitched::DataFormats_TestObjects does not export its SOA dependency: ${test_links}")
endif()

# Evaluate imported include and header file-set paths in the consumer context.
get_property(imported_targets DIRECTORY PROPERTY IMPORTED_TARGETS)
foreach(target IN LISTS imported_targets)
  if(NOT target MATCHES "^Stitched::")
    continue()
  endif()
  set(properties INTERFACE_INCLUDE_DIRECTORIES INTERFACE_SYSTEM_INCLUDE_DIRECTORIES)
  get_target_property(sets "${target}" INTERFACE_HEADER_SETS)
  if(sets)
    foreach(set_name IN LISTS sets)
      if(set_name STREQUAL "HEADERS")
        list(APPEND properties HEADER_DIRS HEADER_SET)
      else()
        list(APPEND properties "HEADER_DIRS_${set_name}" "HEADER_SET_${set_name}")
      endif()
    endforeach()
  endif()
  foreach(property IN LISTS properties)
    get_target_property(value "${target}" "${property}")
    if(value)
      file(GENERATE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/paths/${target}-${property}-$<CONFIG>.txt"
        CONTENT "$<TARGET_GENEX_EVAL:${target},${value}>")
    endif()
  endforeach()
endforeach()

add_executable(reader reader.cc)
target_link_libraries(reader PRIVATE Stitched::FWCore_ParameterSetReader)
add_executable(python_parameters python_parameters.cc)
target_link_libraries(python_parameters PRIVATE Stitched::FWCore_PythonParameterSet)
add_executable(soa soa.cc)
target_link_libraries(soa PRIVATE Stitched::FWCore_SOA)
add_executable(test_objects test_objects.cc)
target_link_libraries(test_objects PRIVATE Stitched::DataFormats_TestObjects)
'''


def run(command, env, description):
    print("+", " ".join(shlex.quote(str(arg)) for arg in command), flush=True)
    try:
        subprocess.run(command, env=env, check=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"{description} failed (exit {error.returncode})") from error


def read_cache(build):
    cache_path = build / "CMakeCache.txt"
    cache = {}
    for line in cache_path.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith(("#", "//")) and "=" in line:
            key, value = line.split("=", 1)
            if ":" in key:
                cache[key.split(":", 1)[0]] = value
    for key in ("CMAKE_HOME_DIRECTORY", "CMAKE_INSTALL_INCLUDEDIR", "CMAKE_INSTALL_LIBDIR"):
        if not cache.get(key):
            raise RuntimeError(f"{cache_path}: missing {key}")
    return cache


def relative_install_dir(cache, key):
    path = Path(cache[key])
    if path.is_absolute() or ".." in path.parts or "$<" in cache[key]:
        raise RuntimeError(f"{key} must be relative to the prefix for this check: {path}")
    return path


def check_install_dirs(cache):
    for key in ("CMAKE_INSTALL_INCLUDEDIR", "CMAKE_INSTALL_LIBDIR", "CMAKE_INSTALL_BINDIR",
                "STITCHED_INSTALL_PYTHONDIR"):
        if cache.get(key):
            relative_install_dir(cache, key)


def check_inventory(source, include):
    expected = set()
    for subsystem in ("FWCore", "DataFormats"):
        root = source / subsystem
        if not root.is_dir():
            raise RuntimeError(f"Source subsystem not found: {root}")
        for interface in root.glob("*/interface"):
            if interface.is_dir():
                expected.update(path.relative_to(source) for path in interface.rglob("*")
                                if path.is_file() and path.suffix in (".h", ".icc"))
    if EXCEPTION not in expected:
        raise RuntimeError(f"Expected source exception not found: {source / EXCEPTION}")
    missing = sorted(path for path in expected - {EXCEPTION} if not (include / path).is_file())
    for path in missing:
        print(f"Missing installed header: {include / path}", file=sys.stderr)
    if (include / EXCEPTION).exists():
        print(f"Private header unexpectedly installed: {include / EXCEPTION}", file=sys.stderr)
    elif not missing:
        print(f"Header inventory: {len(expected) - 1} installed, 1 intentional exception")
        return
    raise RuntimeError("Header inventory failed")


def check_imported_paths(build, prefix):
    path_files = list((build / "paths").glob("*.txt"))
    if not path_files:
        raise RuntimeError("No imported Stitched include/header paths were generated")
    errors = []
    prefix = prefix.resolve()
    for path_file in path_files:
        for entry in path_file.read_text(encoding="utf-8").split(";"):
            if not entry:
                continue
            path = Path(entry)
            try:
                if not path.is_absolute():
                    raise ValueError("not absolute")
                path.resolve().relative_to(prefix)
            except ValueError:
                errors.append(f"{path_file.name}: {entry}")
    if errors:
        for error in errors:
            print(f"Imported path outside staged prefix: {error}", file=sys.stderr)
        raise RuntimeError("Imported include/header path check failed")
    print(f"Checked imported include/header paths in {len(path_files)} metadata files")


def main():
    parser = argparse.ArgumentParser(
        description="Check a built Stitched installation and isolated downstream consumers.",
        epilog="Example: %(prog)s /path/to/build -- -DCMAKE_PREFIX_PATH=/path/to/deps "
               "-DCMAKE_TOOLCHAIN_FILE=/path/to/toolchain.cmake\n"
               "CMake updates the supplied build's install_manifest.txt during installation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("build_dir", type=Path, help="configured and fully built Stitched build directory")
    parser.add_argument("--config", help="build configuration to install and build (place before build_dir)")
    parser.add_argument("--cmake", default="cmake", help="CMake executable to use (place before build_dir)")
    parser.add_argument("cmake_args", nargs=argparse.REMAINDER,
                        help="downstream CMake configure arguments, after --")
    args = parser.parse_args()
    cmake_args = args.cmake_args
    if cmake_args and cmake_args[0] == "--":
        cmake_args = cmake_args[1:]

    build = args.build_dir.resolve()
    cache = read_cache(build)
    source = Path(cache["CMAKE_HOME_DIRECTORY"]).resolve()
    check_install_dirs(cache)
    include_dir = relative_install_dir(cache, "CMAKE_INSTALL_INCLUDEDIR")
    lib_dir = relative_install_dir(cache, "CMAKE_INSTALL_LIBDIR")
    env = os.environ.copy()
    env.pop("CPATH", None)
    env.pop("CPLUS_INCLUDE_PATH", None)

    with tempfile.TemporaryDirectory(prefix="stitched-header-check-") as temporary:
        temp = Path(temporary)
        requested_prefix = temp / "prefix"
        # DESTDIR confines even absolute install destinations to the temporary area.
        install_env = env.copy()
        install_env["DESTDIR"] = str(temp / "destdir")
        prefix = temp / "destdir" / requested_prefix.relative_to(requested_prefix.anchor)
        install_command = [args.cmake, "--install", str(build), "--prefix", str(requested_prefix)]
        if args.config:
            install_command.extend(["--config", args.config])
        run(install_command,
            install_env, "Installation (is the build complete?)")
        check_inventory(source, prefix / include_dir)
        config_dir = prefix / lib_dir / "cmake" / "Stitched"
        if not (config_dir / "StitchedConfig.cmake").is_file():
            raise RuntimeError(f"Installed Stitched config not found: {config_dir}")

        consumer_source = temp / "consumer"
        consumer_build = temp / "consumer-build"
        consumer_source.mkdir()
        (consumer_source / "CMakeLists.txt").write_text(CMAKE_PROJECT, encoding="utf-8")
        for name, content in PROBES.items():
            (consumer_source / f"{name}.cc").write_text(content, encoding="utf-8")
        env.pop("DESTDIR", None)
        run([args.cmake, "-S", str(consumer_source), "-B", str(consumer_build), *cmake_args,
             f"-DSTAGED_CONFIG_DIR:PATH={config_dir}",
             f"-DStitched_DIR:PATH={config_dir}",
             "-DCMAKE_FIND_USE_PACKAGE_REGISTRY:BOOL=OFF",
             "-DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY:BOOL=OFF"], env,
            "Downstream configuration")
        check_imported_paths(consumer_build, prefix)
        build_command = [args.cmake, "--build", str(consumer_build)]
        if args.config:
            build_command.extend(["--config", args.config])
        run(build_command, env, "Downstream compile/link")
    print("Installed header and consumer checks passed")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
