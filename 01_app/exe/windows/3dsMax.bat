:: 3DsMax

:: Hide Commands
@echo off

:: --- PATH ---
set "PROJECT_ROOT=../.."
set "PIPELINEPATH=%PROJECT_ROOT%/dev"

:: --- PYTHON ---
set "PYTHONPATH=%PROJECT_ROOT%/dev"
set "ADSK_3DSMAX_STARTUPSCRIPTS_ADDON_DIR=%PYTHONPATH%" 

set "MAX_VERSION=2022"

:: --- CALL MAX ---
set "MAX_DIR=C:/Program Files/Autodesk/3ds Max %MAX_VERSION%"
set "PATH=%MAX_DIR%"
start "" "%MAX_DIR%/3dsmax.exe"