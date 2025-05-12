# tests/update_keywords_for_all_notes.py

import json
from pathlib import Path
from app.utils.keyword_extractor import extract_keywords

NOTES_DIR = Path("data/notes")

def update_keywords_for_all_notes():
    if not NOTES_DIR.exists():
        print(f"❌ Dossier introuvable : {NOTES_DIR}")
        return

    updated_count = 0

    for note_file in NOTES_DIR.glob("*.json"):
        try:
            with open(note_file, "r", encoding="utf-8") as f:
                note = json.load(f)

            description = note.get("description", "")
            new_keywords = extract_keywords(description)
            note["keywords"] = new_keywords

            with open(note_file, "w", encoding="utf-8") as f:
                json.dump(note, f, ensure_ascii=False, indent=4)

            print(f"🔁 Keywords mis à jour pour {note_file.name}")
            updated_count += 1

        except Exception as e:
            print(f"⚠️ Erreur avec {note_file.name} : {e}")

    print(f"\n✅ {updated_count} notes mises à jour avec succès.")

if __name__ == "__main__":
    update_keywords_for_all_notes()
