cmake_minimum_required(VERSION 3.16)
project(decolink LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Multimedia Network SerialPort)

# icona dell'eseguibile (Esplora risorse / barra applicazioni)
if(WIN32)
    enable_language(RC)
    set(APP_ICON_RC hfgw.rc)
endif()

qt_add_executable(decolink WIN32 main.cpp hfgw.qrc ${APP_ICON_RC})
target_link_libraries(decolink PRIVATE Qt6::Widgets Qt6::Multimedia Qt6::Network Qt6::SerialPort)
