echo off

setlocal enabledelayedexpansion

rem Get the directory of the currently running script
set "SCRIPT_DIR=%~dp0"

echo The script directory is: %SCRIPT_DIR%

dir %SCRIPT_DIR%


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
	
	rem del %1.tag
	
	echo ----------------------------------------
	echo ----------------------------------------
    pause
	exit
) 

if "!EXTEN!"==".js" (  REM JAVASCRIPT

    echo Using Javascript
	ECHO PARSING ...
	python %SCRIPT_DIR%VFCtagger.py  javascript %1
	ECHO POST PROCESSING ...
	python %SCRIPT_DIR%postProcess.py %1.tag "#"
	del %1.tag
	
	echo ----------------------------------------
	echo ----------------------------------------
    pause	
	exit
) 

echo ----------------------------------------
echo ----------------------------------------
echo No language module aviaalable for parsing %1
echo ----------------------------------------
echo ----------------------------------------

pause