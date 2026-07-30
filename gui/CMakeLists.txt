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

# codec2: porta sia la voce a 700 bit/s sia il modem OFDM di FreeDV, che sono le
# due meta' del collegamento d'emergenza. Se manca, il resto funziona comunque:
# il profilo EMRG semplicemente non compare fra le scelte.
if(PkgConfig_FOUND)
    pkg_check_modules(CODEC2 QUIET codec2)
endif()
if(NOT CODEC2_FOUND)
    find_path(CODEC2_INCLUDE_DIR codec2/freedv_api.h)
    find_library(CODEC2_LIBRARY NAMES codec2)
    if(CODEC2_INCLUDE_DIR AND CODEC2_LIBRARY)
        set(CODEC2_INCLUDE_DIRS ${CODEC2_INCLUDE_DIR})
        set(CODEC2_LIBRARIES ${CODEC2_LIBRARY})
        set(CODEC2_FOUND TRUE)
    endif()
endif()
if(CODEC2_FOUND)
    message(STATUS "libcodec2: ${CODEC2_LIBRARIES} (collegamento d'emergenza disponibile)")
else()
    message(WARNING "libcodec2 non trovata: niente collegamento d'emergenza. Su MSYS2:\n"
                    "    pacman -S mingw-w64-x86_64-codec2")
endif()

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
if(CODEC2_FOUND)
    target_compile_definitions(decolink PRIVATE DECOLINK_CON_FREEDV)
    target_include_directories(decolink PRIVATE ${CODEC2_INCLUDE_DIRS})
    target_link_directories(decolink PRIVATE ${CODEC2_LIBRARY_DIRS})
    target_link_libraries(decolink PRIVATE ${CODEC2_LIBRARIES})
endif()
