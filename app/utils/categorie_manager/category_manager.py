import json
from pathlib import Path
from collections import defaultdict

class CategoryManager:
    def __init__(self, notes_path="data/notes", output_path="data/categories"):
        self.notes_path = Path(notes_path)
        self.output_path = Path(output_path)
        self.notes = []
        self.category_notes = defaultdict(list)
        self.note_keywords = {}

    def load_notes(self):
        self.notes.clear()
        self.category_notes.clear()
        self.note_keywords.clear()

        if not self.notes_path.exists():
            print(f"⚠️ Le dossier {self.notes_path} n'existe pas.")
            return

        for note_file in self.notes_path.glob("*.json"):
            try:
                with open(note_file, "r", encoding="utf-8") as f:
                    note = json.load(f)
                    note_id = note.get("id", note_file.stem)
                    keywords = note.get("keywords", [])
                    self.notes.append(note)
                    self.note_keywords[note_id] = keywords
                    for keyword in keywords:
                        self.category_notes[keyword].append(note_id)
            except Exception as e:
                print(f"Erreur de lecture du fichier {note_file.name} : {e}")

    def save_all_categories(self):
        self.output_path.mkdir(parents=True, exist_ok=True)
        all_categories = sorted(self.category_notes.keys())
        all_categories_path = self.output_path / "all_categories.json"

        with open(all_categories_path, "w", encoding="utf-8") as f:
            json.dump({"all_categories": all_categories}, f, indent=4, ensure_ascii=False)
        print(f"✅ all_categories.json mis à jour ({len(all_categories)} catégories).")

    def save_links(self):
        link_data = {}
        for category, notes in self.category_notes.items():
            linked_categories = set()
            for note_id in notes:
                for other_cat in self.note_keywords[note_id]:
                    if other_cat != category:
                        linked_categories.add(other_cat)
            link_data[f"catégories connectées à {category}"] = sorted(linked_categories)
            link_data[f"notes connectées à {category}"] = notes

        link_categories_path = self.output_path / "link_categories.json"
        with open(link_categories_path, "w", encoding="utf-8") as f:
            json.dump(link_data, f, indent=4, ensure_ascii=False)
        print(f"✅ link_categories.json mis à jour.")

    def update(self):
        self.load_notes()
        self.save_all_categories()
        self.save_links()

# Utilisation manuelle (par exemple depuis un script temporaire ou un bouton dev)
if __name__ == "__main__":
    manager = CategoryManager()
    manager.update()
