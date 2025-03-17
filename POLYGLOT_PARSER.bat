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
	
	python %SCRIPT_DIR%VFCtagger.py   python %1   rem add --skip flag to see the raw tags
	ECHO POST PROCESSING ...
	python %SCRIPT_DIR%postProcess.py %1.tag "#"  rem skip this step if using the --skip flag above
	
	del %1.tag  rem comment this to see more intermediate tags when debugging using --skip flag
	
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
	python %SCRIPT_DIR%postProcess.py %1.tag "//"
	
	del %1.tag  rem comment this to see more intermediate tags
	
	echo ----------------------------------------
	echo ----------------------------------------
    pause	
	exit
) 

echo ----------------------------------------
echo ----------------------------------------
echo No language module for parsing %1
echo ----------------------------------------
echo ----------------------------------------

pause