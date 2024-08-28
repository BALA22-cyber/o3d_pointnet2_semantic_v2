cmake_minimum_required(VERSION 3.10)
project(Open3D_PointNet2_Semantic3D)

# Specify C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set CUDA architecture (adjust according to your GPU)
set(CUDA_ARCHITECTURES "61") # Replace "61" with your GPU's compute capability

# Include directories
find_package(CUDA REQUIRED)
find_package(TensorFlow REQUIRED)

include_directories(${TensorFlow_INCLUDE_DIRS})
include_directories(${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES})

# Add source files
set(SOURCE_FILES
    tf_grouping.cpp
    tf_grouping.cu
)

# Create the CUDA target
add_library(tf_grouping SHARED ${SOURCE_FILES})

# Link TensorFlow
target_link_libraries(tf_grouping ${TensorFlow_LIBRARIES})

# Specify CUDA properties
set_target_properties(tf_grouping PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    POSITION_INDEPENDENT_CODE ON
)

# Add the CUDA and C++ flags
target_compile_options(tf_grouping PRIVATE
    $<$<COMPILE_LANGUAGE:CUDA>:--expt-relaxed-constexpr -std=c++17>
    $<$<COMPILE_LANGUAGE:CXX>:-std=c++17>
)

# Set additional properties for the CUDA target
set_target_properties(tf_grouping PROPERTIES CUDA_ARCHITECTURES ${CUDA_ARCHITECTURES})

# Include the OpenMP library if needed
find_package(OpenMP REQUIRED)
if(OpenMP_CXX_FOUND)
    target_link_libraries(tf_grouping PUBLIC OpenMP::OpenMP_CXX)
endif()

# Install the library
install(TARGETS tf_grouping DESTINATION lib)
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/ DESTINATION include)





changes made from tf1 to tf2

changed c++ from 11 to c14


-- Configuring done
CMake Warning (dev) in CMakeLists.txt:
  Policy CMP0104 is not set: CMAKE_CUDA_ARCHITECTURES now detected for NVCC,
  empty CUDA_ARCHITECTURES not allowed.  Run "cmake --help-policy CMP0104"
  for policy details.  Use the cmake_policy command to set the policy and
  suppress this warning.

  CUDA_ARCHITECTURES is empty for target "tf_grouping".
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) in CMakeLists.txt:
  Policy CMP0104 is not set: CMAKE_CUDA_ARCHITECTURES now detected for NVCC,
  empty CUDA_ARCHITECTURES not allowed.  Run "cmake --help-policy CMP0104"
  for policy details.  Use the cmake_policy command to set the policy and
  suppress this warning.

  CUDA_ARCHITECTURES is empty for target "tf_grouping".
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) in CMakeLists.txt:
  Policy CMP0104 is not set: CMAKE_CUDA_ARCHITECTURES now detected for NVCC,
  empty CUDA_ARCHITECTURES not allowed.  Run "cmake --help-policy CMP0104"
  for policy details.  Use the cmake_policy command to set the policy and
  suppress this warning.

  CUDA_ARCHITECTURES is empty for target "tf_sampling".
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) in CMakeLists.txt:
  Policy CMP0104 is not set: CMAKE_CUDA_ARCHITECTURES now detected for NVCC,
  empty CUDA_ARCHITECTURES not allowed.  Run "cmake --help-policy CMP0104"
  for policy details.  Use the cmake_policy command to set the policy and
  suppress this warning.

  CUDA_ARCHITECTURES is empty for target "tf_sampling".
This warning is for project developers.  Use -Wno-dev to suppress it.