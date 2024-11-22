@echo off

set PYTHON=".venv\Scripts\Python.exe"
echo venv %PYTHON%

%PYTHON% main.py %*

exit
