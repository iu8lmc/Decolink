@echo off
rem %~dp0 e' la cartella di questo file: cosi' lo script funziona da dove si
rem trova, senza un percorso scritto a mano che si rompe al primo spostamento.
set "PATH=C:\msys64\mingw64\bin;%PATH%"
cd /d "%~dp0"
if not exist build mkdir build
cd build
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release .. || exit /b 1
mingw32-make -j8 || exit /b 1
