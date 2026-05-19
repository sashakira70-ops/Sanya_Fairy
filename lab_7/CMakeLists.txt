cmake_minimum_required(VERSION 3.10)
project(Lab7_CV_Multithreading)

set(CMAKE_CXX_STANDARD 14)

find_package(OpenCV REQUIRED)
find_package(Threads REQUIRED)

add_executable(lab7 main.cpp FaceDetector.cpp)
target_link_libraries(lab7 ${OpenCV_LIBS} Threads::Threads)
