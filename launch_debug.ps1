# 🔥 Le chemin de ton python.exe AVEC des guillemets
$pythonExe = ".\venv\Scripts\python.exe"

# Vérification si l'exécutable existe
if (!(Test-Path $pythonExe)) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show("❌ Le venv n'existe pas.`nLance 'setup_venv.bat' d'abord.", "Erreur")
    exit
}

# Exécuter main.py avec le bon python.exe
& "$pythonExe" "launcher.py"

Pause
