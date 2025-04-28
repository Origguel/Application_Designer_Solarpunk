@echo off
REM ➔ Aller dans le dossier assets
cd /d C:\Users\origg\Documents\GitHub\Application_Designer_Solarpunk\assets

REM ➔ Activer l'environnement virtuel
call ..\venv\Scripts\activate

REM ➔ Compiler le fichier resources.qrc
..\venv\Scripts\pyside6-rcc.exe resources.qrc -o ..\app\resources_rc.py

IF %ERRORLEVEL% EQU 0 (
    echo ✅ Compilation terminee avec succes !
) ELSE (
    echo ❌ Erreur pendant la compilation !
)

pause
