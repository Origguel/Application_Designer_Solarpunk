"""
Controleur pour ajouter, supprimer et charger les notes.
"""
import json
from pathlib import Path
from app.models.note_model import NoteModel

DATA_FOLDER = Path("data/notes/")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

class NoteController:

    @staticmethod
    def save_note(note: NoteModel):
        path = DATA_FOLDER / f"{note.id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(note.__dict__, f, ensure_ascii=False, indent=4)

    @staticmethod
    def load_notes():
        notes = []
        for file in DATA_FOLDER.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                notes.append(NoteModel(**data))
        return notes