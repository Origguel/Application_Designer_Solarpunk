from pathlib import Path
import json

class TimelineDataLoader:
    def __init__(self, index_path="data/timeline/note_index_by_date.json", notes_folder="data/notes"):
        self.index_path = Path(index_path)
        self.notes_folder = Path(notes_folder)
        self.note_index = self.load_index()
        self.note_cache = {}

    def load_index(self):
        if not self.index_path.exists():
            print("❌ Fichier d'index de notes introuvable")
            return {}
        with open(self.index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_notes_for_date(self, date_obj):
        date_str = date_obj.strftime("%Y-%m-%d")
        note_ids = self.note_index.get(date_str, [])
        notes = []
        for note_id in note_ids:
            if note_id in self.note_cache:
                notes.append(self.note_cache[note_id])
            else:
                try:
                    with open(self.notes_folder / f"{note_id}.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.note_cache[note_id] = data
                        notes.append(data)
                except Exception as e:
                    print(f"❌ Note manquante : {note_id}")
        return notes
