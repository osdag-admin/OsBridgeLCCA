@echo off
echo Creating and activating Conda environment...

REM Try activating the environment
call conda activate osbridgelcca 2>nul
if errorlevel 1 (
    echo Environment not found. Creating it now...
    call conda create -n osbridgelcca python=3.9 -y
    call conda activate osbridgelcca
)

echo Installing dependencies from pyproject.toml...
pip install .

echo Installation complete!
python scripts\verify_installation.py
