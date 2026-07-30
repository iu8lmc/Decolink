cmake_minimum_required(VERSION 3.16)
project(decolink LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Multimedia Network SerialPort)

# Opus: la fonia passa da 786 a ~28 kbit/s. Arriva con MSYS2 (mingw-w64-opus) e
# lo porta gia' Qt Multimedia, quindi non aggiunge nulla al pacchetto: la DLL
# c'e' comunque. Si cerca prima con pkg-config, che e' il modo in cui opus si
# descrive; il ripiego serve sui sistemi che non ce l'hanno.
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(OPUS QUIET opus)
endif()
if(NOT OPUS_FOUND)
    find_path(OPUS_INCLUDE_DIR opus.h PATH_SUFFIXES opus)
    find_library(OPUS_LIBRARY NAMES opus)
    if(OPUS_INCLUDE_DIR AND OPUS_LIBRARY)
        set(OPUS_INCLUDE_DIRS ${OPUS_INCLUDE_DIR})
        set(OPUS_LIBRARIES ${OPUS_LIBRARY})
        set(OPUS_FOUND TRUE)
    endif()
endif()
if(NOT OPUS_FOUND)
    message(FATAL_ERROR "libopus non trovata: serve al profilo voce. Su MSYS2:\n"
                        "    pacman -S mingw-w64-x86_64-opus")
endif()
message(STATUS "libopus: ${OPUS_LIBRARIES}")

# icona dell'eseguibile (Esplora risorse / barra applicazioni)
if(WIN32)
    enable_language(RC)
    set(APP_ICON_RC hfgw.rc)
endif()

qt_add_executable(decolink WIN32 main.cpp hfgw.qrc ${APP_ICON_RC})
target_include_directories(decolink PRIVATE ${OPUS_INCLUDE_DIRS})
target_link_directories(decolink PRIVATE ${OPUS_LIBRARY_DIRS})
target_link_libraries(decolink PRIVATE Qt6::Widgets Qt6::Multimedia Qt6::Network Qt6::SerialPort
                                       ${OPUS_LIBRARIES})
