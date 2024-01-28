:: 3DsMax

:: Hide Commands
@echo off

:: --- PATH ---
set "PIPELINEPATH=%~dp0"

:: --- PYTHON ---
set "PYTHONPATH=%PIPELINEPATH:~0,-1%\dev"
set "ADSK_3DSMAX_STARTUPSCRIPTS_ADDON_DIR=%PYTHONPATH%" 

set "MAX_VERSION=2022"

:: --- CALL MAX ---
set "MAX_DIR=C:/Program Files/Autodesk/3ds Max %MAX_VERSION%"
set "PATH=%MAX_DIR%"
start "" "%MAX_DIR%/3dsmax.exe"

