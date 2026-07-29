@echo off
cd /d "C:\decolink\gui\build"
"C:\decolink\gui\build\decolink.exe" --cattest COM5 38400 > _c.txt 2>&1
echo exitcode=%errorlevel%
type _c.txt
del _c.txt
