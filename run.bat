@echo off
REM Quick run script for Windows

cd /d "%~dp0"
call venv\Scripts\activate.bat
python convert.py
pause
