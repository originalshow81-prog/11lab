@echo off
echo Pornesc botul Telegram TTS...
echo.

REM Verifica daca .env exista
if not exist ".env" (
    echo EROARE: Fisierul .env nu exista!
    echo Copiaza .env.example in .env si completeaza cheile.
    pause
    exit /b 1
)

REM Instaleaza dependentele daca nu sunt instalate
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo Instalez dependentele...
    pip install -r requirements.txt
)

echo Bot pornit! Lasa aceasta fereastra deschisa.
echo Apasa Ctrl+C pentru oprire.
echo.
python bot.py
pause
