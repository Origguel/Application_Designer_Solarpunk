import json
from pathlib import Path

SELECTION_PATH = Path("assets/note_selection/selected_note.json")


def get_selected_note_id():
    """Retourne l'ID de la note sélectionnée actuellement."""
    if not SELECTION_PATH.exists():
        return None
    try:
        with open(SELECTION_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("note_id_selected", None)
    except Exception as e:
        print(f"❌ Erreur lecture selected_note.json : {e}")
        return None

def set_selected_note_id(note_id: str):
    """Met à jour l'ID de la note sélectionnée."""
    try:
        with open(SELECTION_PATH, "w", encoding="utf-8") as f:
            json.dump({"note_id_selected": note_id}, f, indent=4)
    except Exception as e:
        print(f"❌ Erreur écriture selected_note.json : {e}")