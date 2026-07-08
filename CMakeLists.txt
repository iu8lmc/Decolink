cmake_minimum_required(VERSION 3.16)
project(hf-gateway CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

add_executable(hf-gateway src/main.cpp)

if(WIN32)
  target_link_libraries(hf-gateway ws2_32 ole32)
  # exe singolo senza DLL di runtime
  target_link_options(hf-gateway PRIVATE -static -static-libgcc -static-libstdc++)
elseif(APPLE)
  target_link_libraries(hf-gateway
    "-framework CoreFoundation" "-framework CoreAudio" "-framework AudioToolbox"
    pthread m)
else() # Linux
  target_link_libraries(hf-gateway pthread m dl)
endif()
