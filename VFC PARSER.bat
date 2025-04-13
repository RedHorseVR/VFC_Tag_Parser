

python C:\Users\luisr\VFC_Tag_Parser\VFCtagger.py %1

echo off
set filepath=%1
for %%A in ("%filepath%") do set filename=%%~nxA
echo Filename: %filename%

copy %filename% _%filename%

dir

pause