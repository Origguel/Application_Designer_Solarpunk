import json
from pathlib import Path


class CategoryTreeUpdater:
    def __init__(self, tree_path="data/categories/category_tree.json"):
        self.tree_path = Path(tree_path)
        if not self.tree_path.exists():
            raise FileNotFoundError(f"Fichier {self.tree_path} introuvable.")
        with open(self.tree_path, "r", encoding="utf-8") as f:
            self.tree = json.load(f)

    def save(self):
        with open(self.tree_path, "w", encoding="utf-8") as f:
            json.dump(self.tree, f, indent=4, ensure_ascii=False)
        print("✅ Arbre mis à jour.")

    def add_note(self, note_id, keywords):
        for keyword in keywords:
            node = self._find_or_create_category(self.tree, keyword)
            if note_id not in node["notes"]:
                node["notes"].append(note_id)
                print(f"➕ Ajouté {note_id} à {keyword}")
        self.save()

    def delete_note(self, note_id):
        modified = self._remove_note_recursive(self.tree, note_id)
        if modified:
            print(f"❌ Supprimé {note_id} de l'arbre.")
            self.save()
        else:
            print(f"⚠️ Note {note_id} introuvable.")

    def _remove_note_recursive(self, node, note_id):
        modified = False
        if "notes" in node and note_id in node["notes"]:
            node["notes"].remove(note_id)
            modified = True
        for child in node.get("children", []):
            if self._remove_note_recursive(child, note_id):
                modified = True
        return modified

    def _find_or_create_category(self, current_node, category_name):
        # Recherche récursive de la catégorie
        for child in current_node.get("children", []):
            if child["name"].lower() == category_name.lower():
                return child
            result = self._find_or_create_category(child, category_name)
            if result:
                return result

        # Si non trouvée, créer à la racine
        new_node = {
            "name": category_name,
            "type": "category",
            "notes": [],
            "children": []
        }
        current_node.setdefault("children", []).append(new_node)
        print(f"📁 Création de la catégorie : {category_name}")
        return new_node
