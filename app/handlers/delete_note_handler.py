import os
from PySide6.QtWidgets import QMessageBox

from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater



def confirm_and_delete_note(parent_view, selected_note_id):
    if not selected_note_id:
        QMessageBox.warning(parent_view, "Pas de sélection", "Aucune note sélectionnée à supprimer.")
        return

    confirm = QMessageBox.question(
        parent_view,
        "Supprimer la note",
        f"Voulez-vous vraiment supprimer la note ID {selected_note_id} ?",
        QMessageBox.Yes | QMessageBox.No
    )

    if confirm == QMessageBox.Yes:
        delete_note_file(selected_note_id)
        parent_view.refresh_graph()

def delete_note_file(note_id):
    file_path = os.path.join("data", "notes", f"{note_id}.json")

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🗑️ Note ID {note_id} supprimée avec succès.")

        CategoryTreeUpdater().delete_note(note_id)  # ➖ Retire du tree
        from app.utils.categorie_manager.category_manager import CategoryManager
        CategoryManager().update()  # 🔁 Met à jour les fichiers de lien/catégories
    else:
        print(f"❌ Le fichier de la note ID {note_id} est introuvable.")
