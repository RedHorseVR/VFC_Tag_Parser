echo off

setlocal enabledelayedexpansion

rem Get the directory of the currently running script
set "SCRIPT_DIR=%~dp0"

echo The script directory is: %SCRIPT_DIR%

dir %SCRIPT_DIR%

set "SCRIPT_DIR=E:\Users\luisr\OneDrive\Desktop\VFC_Tag_Parser\"

for %%A in ("%1") do (
    set "EXTEN=%%~xA"
)
echo ----------------------------------------
echo ----------------------------------------
echo POLYGLOT PARSER SEES EXTENSION: !EXTEN!


if "!EXTEN!"==".py" (  REM PYTHON

    echo Using Python ...
	ECHO TAG PARSING ...
	
	python %SCRIPT_DIR%VFCtagger.py   python %1
	ECHO POST PROCESSING ...
	python %SCRIPT_DIR%postProcess.py %1.tag "#"
	
	del %1.tag
	
	echo PY ----------------------------------------
	echo ----------------------------------------
    rem pause
	rem exit
) 

if "!EXTEN!"==".ts" (  REM TYPE SCRIPT

    echo Using typescript ...
	ECHO TAG PARSING ...
	
	python %SCRIPT_DIR%VFCtagger.py   javascript %1
	ECHO POST PROCESSING ...
	python %SCRIPT_DIR%postProcess.py %1.tag "#"
	
	del %1.tag
	
	echo TS ----------------------------------------
	echo ----------------------------------------
    rem pause
	rem exit
) 

if "!EXTEN!"==".js" (  REM JAVASCRIPT

    echo Using Javascript
	ECHO PARSING ...
	python %SCRIPT_DIR%VFCtagger.py  javascript %1
	ECHO POST PROCESSING ...
	python %SCRIPT_DIR%postProcess.py %1.tag "//"
	
	del %1.tag
	
	echo JS ----------------------------------------
	echo ----------------------------------------
    rem pause	
	rem exit
) 

echo ----------------------------------------
echo ----------------------------------------
echo done parsing %1
echo ----------------------------------------
echo ----------------------------------------

START VFC2000 %1.tag.vfc -Reload

EXIT
 REM pause