# tests/rebuild_categories_and_tree.py

from app.utils.categorie_manager.category_manager import CategoryManager
from app.utils.categorie_manager.tree_structure_generator import TreeStructureGenerator

def rebuild_all():
    print("📂 Mise à jour des catégories et des liens...")
    manager = CategoryManager()
    manager.update()

    print("🌳 Reconstruction de l'arbre des catégories...")
    generator = TreeStructureGenerator()
    generator.generate()

    print("✅ Reconstruction terminée.")

if __name__ == "__main__":
    rebuild_all()
