project(pylena CXX)
cmake_minimum_required(VERSION 3.14)

include(FetchContent)
FetchContent_Declare(pybind11
URL https://github.com/pybind/pybind11/archive/refs/tags/v2.6.2.zip
URL_HASH MD5=b17cb3a42dc1e7cf5f0f1107d44d853c)
FetchContent_MakeAvailable(pybind11)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_BINARY_DIR})

set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 20)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

find_package(PythonInterp 3 REQUIRED)
find_package(Pylene REQUIRED COMPONENTS Pylene-numpy)

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pylena)
