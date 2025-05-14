import json
from pathlib import Path
from app.components.note.add_note_widget import AddNoteWidget
from app.components.note.note_detail_widget import NoteDetailWidget
from app.utils.categorie_manager.category_manager import CategoryManager
from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater
from app.handlers.delete_note_handler import confirm_and_delete_note

def open_note_detail(self, note_id):
    note_path = Path(f"data/notes/{note_id}.json")
    if not note_path.exists():
        print(f"❌ Fichier de note introuvable : {note_path}")
        return

    with open(note_path, "r", encoding="utf-8") as f:
        note_data = json.load(f)

    self.close_note_detail()  # supprime l'ancien s'il existe

    # Crée le nouveau widget D'ABORD
    self.note_detail_widget = NoteDetailWidget(note_data, self)

    # Calcule ensuite sa position
    widget_width = 460
    top_margin = self.note_detail_top_margin     # sous la toolbar
    left_margin = self.note_detail_left_margin   # à droite des outils
    bottom_margin = 26
    available_height = self.height() - top_margin - bottom_margin

    self.note_detail_widget.setGeometry(
        left_margin,
        top_margin,
        widget_width,
        available_height
    )

    self.note_detail_widget.raise_()
    self.note_detail_widget.show()




def close_note_detail(self):
    if hasattr(self, 'note_detail_widget') and self.note_detail_widget:
        self.note_detail_widget.setParent(None)
        self.note_detail_widget.deleteLater()
        self.note_detail_widget = None

def open_add_note_widget(self):
    if not self.add_note_widget:
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.show()
        self.overlay.raise_()

        self.add_note_widget = AddNoteWidget(self)
        w, h = int(self.width() * 0.6), int(self.height() * 0.6)
        self.add_note_widget.setGeometry(
            (self.width() - w) // 2, (self.height() - h) // 2, w, h
        )

        self.add_note_widget.raise_()
        self.add_note_widget.show()
        self.add_note_widget.cancelled.connect(self.close_add_note_widget)
        self.add_note_widget.note_created.connect(self.add_note_visually)

def close_add_note_widget(self):
    if self.add_note_widget:
        self.add_note_widget.setParent(None)
        self.add_note_widget.deleteLater()
        self.add_note_widget = None
    self.overlay.hide()

def on_delete_button_clicked(self):
    selected_note_id = self.graph_widget.get_selected_note_id()
    if selected_note_id:
        confirm_and_delete_note(self, selected_note_id)
        CategoryManager().update()
        self.graph_widget.delete_note_live(selected_note_id)
    else:
        print("❌ Aucune note sélectionnée pour suppression.")

def add_note_visually(self, note_id, keywords):
    updater = CategoryTreeUpdater()
    updater.add_note(note_id, keywords)
    self.graph_widget.add_note_live(note_id, keywords)
    print(f"✨ Note ajoutée visuellement dans le graphe : {note_id}")
    self.close_add_note_widget()
