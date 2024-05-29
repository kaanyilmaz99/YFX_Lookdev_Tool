:: 3DsMax

:: Hide Commands
@echo off

:: --- PATH ---
set "PIPELINEPATH=%~dp0"

:: --- PYTHON ---
set "PYTHONPATH=%PIPELINEPATH:~0,-1%\dev"
set "ADSK_3DSMAX_STARTUPSCRIPTS_ADDON_DIR=%PIPELINEPATH:~0,-1%\dev" 

set "MAX_VERSION=2023"

set "QT_AUTO_SCREEN_SCALE_FACTOR=0"

:: --- SPLASH SCREEN ---
set "SPLASH_IMG=%PIPELINEPATH:~0,-1%\img\3dsMax_2023_YFX_Splashscreen.png"

:: --- CALL MAX ---
set "MAX_DIR=C:/Program Files/Autodesk/3ds Max %MAX_VERSION%"
set "PATH=%MAX_DIR%"
start "" "%MAX_DIR%/3dsmax.exe" -a %SPLASH_IMG%

