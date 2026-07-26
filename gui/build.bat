@echo off
set "PATH=C:\msys64\mingw64\bin;%PATH%"
cd /d C:\hf-gateway\gui
if not exist build mkdir build
cd build
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release .. || exit /b 1
mingw32-make -j8 || exit /b 1
