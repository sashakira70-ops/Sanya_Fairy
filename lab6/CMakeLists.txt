cmake_minimum_required(VERSION 3.10)
project(Lab6)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS} include)

add_executable(Lab6 src/main.cpp src/VideoProcessor.cpp)
target_link_libraries(Lab6 ${OpenCV_LIBS})
