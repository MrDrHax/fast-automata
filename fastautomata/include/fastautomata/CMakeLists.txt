cmake_minimum_required(VERSION 3.12)
project(fastautomata_clib)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find the Python3 package
find_package(Python3 COMPONENTS Development Interpreter REQUIRED)

# Create a library
add_library(fastautomata_lib fastautomata.cpp Board.hpp Agents.cpp ClassTypes.hpp)

# Add the Python3 include directories to the include path
target_include_directories(fastautomata_lib PRIVATE ${Python3_INCLUDE_DIRS})

# Find the pybind11 package
find_package(pybind11 REQUIRED)

# Create a Python module with your bindings
pybind11_add_module(fastautomata_clib MODULE bindings.cpp)

# Link the library to the Python module
target_link_libraries(fastautomata_clib PRIVATE fastautomata_lib stdc++fs)

# Set the output directory for the build libraries
set_target_properties(fastautomata_clib PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../..
)