@echo off
setlocal

python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Pip not installed
    exit /b 1
)

set "packages=tkinter watchdog psutil"

for %%p in (%packages%) do (
    python -c "import %%p" 2>nul
    IF %ERRORLEVEL% NEQ 0 (
        echo Installation of %%p...
        python -m pip install %%p
    )
)

python .\ZipManager.py

endlocal
