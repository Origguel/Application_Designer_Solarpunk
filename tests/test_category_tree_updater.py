import json
import os
from pathlib import Path
from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater

TREE_PATH = Path("data/categories/category_tree.json")
NOTES_DIR = Path("data/notes")

def test_add_and_delete_note():
    test_note_id = "note_test_9999"
    test_keywords = ["testcat1", "testcat2"]

    # Ajout
    updater = CategoryTreeUpdater()
    updater.add_note(test_note_id, test_keywords)

    # Vérification ajout
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        tree = json.load(f)
    assert contains_note(tree, test_note_id), "❌ La note n’a pas été trouvée dans l’arbre après ajout."

    print("✅ Ajout de note vérifié.")

    # Suppression
    updater.delete_note(test_note_id)

    # Vérification suppression
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        tree = json.load(f)
    assert not contains_note(tree, test_note_id), "❌ La note est encore présente après suppression."

    assert not contains_category(tree, "testcat1"), "❌ testcat1 n’a pas été supprimée correctement."
    assert not contains_category(tree, "testcat2"), "❌ testcat2 n’a pas été supprimée correctement."

    print("✅ Suppression et nettoyage vérifiés.")

def contains_note(node, note_id):
    if note_id in node.get("notes", []):
        return True
    for child in node.get("children", []):
        if contains_note(child, note_id):
            return True
    return False

def contains_category(node, category_name):
    if node.get("name", "").lower() == category_name.lower():
        return True
    for child in node.get("children", []):
        if contains_category(child, category_name):
            return True
    return False

if __name__ == "__main__":
    test_add_and_delete_note()
