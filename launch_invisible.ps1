# Active le venv et lance ton appli AVEC console visible (DEBUG MODE)

# Chemin vers le venv
$venvActivate = "venv\Scripts\activate.ps1"

# Vérification que le venv existe
if (!(Test-Path $venvActivate)) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show("❌ L'environnement virtuel est manquant.`nLance 'setup_venv.bat' d'abord.", "Erreur")
    exit
}

# Commande complète pour exécuter visiblement
& {
    & "$venvActivate"
    python main.py
}
