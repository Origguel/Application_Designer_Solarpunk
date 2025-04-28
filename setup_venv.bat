@echo off
REM === Crée un nouvel environnement virtuel nommé "venv" ===
python -m venv venv

REM === Active l'environnement virtuel ===
call venv\Scripts\activate

REM === Met à jour pip (très important !) ===
python -m pip install --upgrade pip

REM === Installe toutes les dépendances listées ===
pip install -r requirements.txt

echo.
echo ✅ Installation terminée !
echo 🚀 Pour lancer ton app, pense à activer ton venv :
echo     venv\Scripts\activate
echo puis lance ton main.py avec :
echo     python main.py
pause
