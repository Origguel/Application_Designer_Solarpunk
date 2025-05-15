import os

IGNORED_FOLDERS = {"__pycache__", ".git", ".vscode", "venv", "env", ".idea"}
IGNORED_FILES = {".DS_Store"}

def lister_structure(dossier, indent=0):
    contenu = []
    for element in sorted(os.listdir(dossier)):
        if element in IGNORED_FILES:
            continue
        chemin = os.path.join(dossier, element)
        if os.path.isdir(chemin):
            if element in IGNORED_FOLDERS:
                continue
            contenu.append("  " * indent + f"[{element}/]")
            contenu.extend(lister_structure(chemin, indent + 1))
        else:
            extension = os.path.splitext(element)[1]
            contenu.append("  " * indent + f"- {element} ({extension})")
    return contenu

if __name__ == "__main__":
    dossier_cible = "."  # Change vers un chemin précis si besoin
    structure = lister_structure(dossier_cible)

    with open("project_structure.txt", "w", encoding="utf-8") as f:
        f.write("Structure du projet:\n\n")
        f.write("\n".join(structure))

    print("✅ Fichier 'project_structure.txt' généré avec succès.")







# cd C:\Users\origg\Documents\GitHub\Application_Designer_Solarpunk
# venv\Scripts\activate
# python -m generate_project_structure