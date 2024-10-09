@echo off
echo Starting Flask application...
C:\Python312\python.exe C:\PythonRoot\BookSearch-81\app.py
if errorlevel 1 (
    echo Application exited with an error.
    pause
) else (
    echo Application exited successfully.
)