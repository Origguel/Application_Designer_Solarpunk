import json
from pathlib import Path
from datetime import datetime
from app.utils.keyword_extractor import extract_keywords

# Links
from app.utils.categorie_manager.category_manager import CategoryManager
from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater


# Dossier de sauvegarde des notes
NOTES_DIR = Path("data/notes/")
NOTES_DIR.mkdir(parents=True, exist_ok=True)


class NoteCreator:
    @staticmethod
    def create_note(title, date_str, note_type, project, description, contenu):
        note_id = NoteCreator.generate_next_id()

        # 🔹 Extraction avancée des mots-clés
        keywords = extract_keywords(description)

        note_data = {
            "id": note_id,
            "date": date_str,
            "title": title,
            "description": description,
            "project": project,
            "keywords": keywords,
            "type": note_type,
            "contenu": contenu
        }

        file_path = NOTES_DIR / f"{note_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(note_data, f, ensure_ascii=False, indent=4)

        # 🆕 Mise à jour des catégories de liens et du tree
        CategoryManager().update()

        # 🆕 Ajout de la note dans le tree JSON
        try:
            updater = CategoryTreeUpdater()
            updater.add_note(note_id, keywords)
        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout de la note au tree : {e}")

        return note_data


    @staticmethod
    def generate_next_id():
        existing_ids = []
        for file in NOTES_DIR.glob("note_*.json"):
            try:
                num = int(file.stem.replace("note_", ""))
                existing_ids.append(num)
            except ValueError:
                continue

        next_id = max(existing_ids, default=0) + 1
        return f"note_{next_id:04d}"
