cmake_minimum_required(VERSION 3.16)
project(hfgw-client LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Multimedia Network)

qt_add_executable(hfgw-client WIN32 main.cpp)
target_link_libraries(hfgw-client PRIVATE Qt6::Widgets Qt6::Multimedia Qt6::Network)
