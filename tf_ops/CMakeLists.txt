cmake_minimum_required(VERSION 3.22 FATAL_ERROR)
set(CMAKE_C_COMPILER "/usr/bin/gcc")
set(CMAKE_CXX_COMPILER "/usr/bin/g++")
project(tf_ops LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Set CMake policies
cmake_policy(SET CMP0074 NEW)

# Open3D cmake
include(open3d.cmake)
message(STATUS "Open3D installed to: ${Open3D_LIBRARY_DIRS}")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${Open3D_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${Open3D_CXX_FLAGS} -O3")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${Open3D_EXE_LINKER_FLAGS}")

# Custom finders path
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR})

# TensorFlow setup
set(TensorFlow_ROOT "/maverick/tf2/lib/python3.10/site-packages/tensorflow")
set(TensorFlow_INCLUDE_DIR "${TensorFlow_ROOT}/include")
# set(TensorFlow_FRAMEWORK_LIBRARY "/home/maverick/miniconda3/envs/tf216/lib/python3.10/site-packages/tensorflow/libtensorflow_framework.so.2")
set(TensorFlow_FRAMEWORK_LIBRARY "/home/maverick/tf2/lib/python3.10/site-packages/tensorflow/libtensorflow_framework.so.2")

find_package(TensorFlow REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -D_GLIBCXX_USE_CXX11_ABI=${TensorFlow_CXX_ABI}")

# **Include Abseil**
include_directories(/usr/local/include)
link_directories(/usr/local/lib)

# CUDA and TensorFlow linking
link_directories(
    ${TensorFlow_ROOT}  # TensorFlow root directory
    ${CMAKE_CUDA_IMPLICIT_LINK_DIRECTORIES}
)
include_directories(
    ${TensorFlow_INCLUDE_DIR}
    ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
)

# Grouping
add_library(tf_grouping SHARED
    tf_grouping.cu
    tf_grouping.cpp
)
target_compile_features(tf_grouping PUBLIC cxx_std_17)
target_link_libraries(tf_grouping cudart ${TensorFlow_FRAMEWORK_LIBRARY})
set_target_properties(tf_grouping PROPERTIES CUDA_SEPARABLE_COMPILATION ON)

# Interpolate
link_directories(${Open3D_LIBRARY_DIRS})
add_library(tf_interpolate SHARED
    tf_interpolate.cpp
)
target_compile_features(tf_interpolate PUBLIC cxx_std_17)
target_include_directories(tf_interpolate PUBLIC ${Open3D_INCLUDE_DIRS})
target_link_libraries(tf_interpolate ${TensorFlow_FRAMEWORK_LIBRARY} ${Open3D_LIBRARIES})

# Sampling
add_library(tf_sampling SHARED
    tf_sampling.cu
    tf_sampling.cpp
)
target_compile_features(tf_sampling PUBLIC cxx_std_17)
target_link_libraries(tf_sampling cudart ${TensorFlow_FRAMEWORK_LIBRARY})
set_target_properties(tf_sampling PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
