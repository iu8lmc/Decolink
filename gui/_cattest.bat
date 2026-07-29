@echo off
rem Prova la seriale del rig senza aprire l'interfaccia: distingue un problema
rem di porta o cablaggio da uno di rete.
cd /d "%~dp0build"
decolink.exe --cattest COM5 38400 > _c.txt 2>&1
echo exitcode=%errorlevel%
type _c.txt
del _c.txt
