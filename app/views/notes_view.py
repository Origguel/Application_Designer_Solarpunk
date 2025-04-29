# app/views/notes_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from app.components.graph_widget import GraphWidget
from app.components.buttons.button_icon import ButtonIcon
from app.components.add_note_widget import AddNoteWidget
from app.handlers.delete_note_handler import confirm_and_delete_note
from app.components.interactive_ellipse_item import InteractiveEllipseItem
from PySide6.QtWidgets import QLineEdit



class NotesView(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Graph principal
        self.graph_widget = GraphWidget(self)
        self.layout.addWidget(self.graph_widget)

        # Overlay blanc semi-transparent pour désactiver le graph
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("""
            background-color: rgba(255, 255, 255, 180);
        """)
        self.overlay.hide()
        self.overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        # Bouton add +
        self.plus_button = ButtonIcon("+", 36, 36, "Button_Secondary", self)
        self.plus_button.move(34, 26)
        self.plus_button.raise_()
        self.plus_button.clicked.connect(self.open_add_note_widget)

        # Bouton delete - 
        self.delete_button = ButtonIcon("-", 36, 36, "Button_Delete", self)
        self.delete_button.move(34, 66)
        self.delete_button.raise_()
        self.delete_button.clicked.connect(self.on_delete_button_clicked)  # 🆕 Connexion du clic

        # Bouton reset r
        self.resetview_button = ButtonIcon("R", 36, 36, "Button_Secondary", self)
        self.resetview_button.move(34, 106)
        self.resetview_button.raise_()
        self.resetview_button.clicked.connect(self.on_reset_view_button_clicked)  # 🆕 Connexion du clic

        # Barre de recherche
        self.search_input = QLineEdit(self)
        self.search_input.setObjectName("search_input")
        self.search_input.setPlaceholderText("Rechercher une note...")
        self.search_input.setFixedWidth(400)
        self.search_input.setFixedHeight(34)
        self.search_input.move(74, 26)
        self.search_input.raise_()
        self.search_input.returnPressed.connect(self.on_search_note)


        # Panneau d'ajout
        self.add_note_widget = None

    def open_add_note_widget(self):
        """Ouvre la fenêtre pour ajouter une nouvelle note"""
        if not self.add_note_widget:
            self.overlay.setGeometry(0, 0, self.width(), self.height())
            self.overlay.show()
            self.overlay.raise_()

            self.add_note_widget = AddNoteWidget(self)
            widget_width = int(self.width() * 0.6)
            widget_height = int(self.height() * 0.6)
            self.add_note_widget.setGeometry(
                (self.width() - widget_width) // 2,
                (self.height() - widget_height) // 2,
                widget_width,
                widget_height
            )

            self.add_note_widget.raise_()
            self.add_note_widget.show()

            # Connecter les signaux
            self.add_note_widget.cancelled.connect(self.close_add_note_widget)
            self.add_note_widget.note_created.connect(self.refresh_graph)

    def close_add_note_widget(self):
        """Ferme proprement la fenêtre d'ajout de note"""
        if self.add_note_widget:
            self.add_note_widget.setParent(None)
            self.add_note_widget.deleteLater()
            self.add_note_widget = None
        self.overlay.hide()

    def resizeEvent(self, event):
        """Adapter la taille des éléments au redimensionnement"""
        super().resizeEvent(event)
        if hasattr(self, 'graph_widget'):
            self.graph_widget.setGeometry(0, 0, self.width(), self.height())
        if hasattr(self, 'plus_button'):
            self.plus_button.move(34, 26)
        if hasattr(self, 'delete_button'):
            self.delete_button.move(34, 66)
        if hasattr(self, 'resetview_button'):
            self.resetview_button.move(34, 106)
        if hasattr(self, 'search_input'):
            self.search_input.move(74, 26)
        if self.overlay.isVisible():
            self.overlay.setGeometry(0, 0, self.width(), self.height())
        if self.add_note_widget:
            self.add_note_widget.move(
                (self.width() - self.add_note_widget.width()) // 2,
                (self.height() - self.add_note_widget.height()) // 2
            )

    def refresh_graph(self):
        """ Recharge complètement le graphe après ajout ou suppression d'une note """
        print("🔄 Rafraîchissement du graphe...")

        InteractiveEllipseItem.selected_item = None

        self.graph_widget.setParent(None)
        self.graph_widget.deleteLater()

        self.graph_widget = GraphWidget(self)
        self.layout.addWidget(self.graph_widget)

        self.plus_button.raise_()
        self.delete_button.raise_()
        self.resetview_button.raise_()  # 🆕 Ajouter ici



    def on_delete_button_clicked(self):
        """Handler appelé quand on clique sur le bouton Delete"""
        selected_note_id = self.graph_widget.get_selected_note_id()
        confirm_and_delete_note(self, selected_note_id)

    def on_reset_view_button_clicked(self):
        """Handler appelé quand on clique sur le bouton Reset View"""
        self.graph_widget.resetTransform()
        self.graph_widget.centerOn(0, 0)
        print("🧹 Vue du graphe réinitialisée.")


    def on_search_note(self):
        """Handler appelé quand on valide une recherche"""
        keyword = self.search_input.text().strip().lower()

        if not keyword:
            return

        # D'abord, retirer tous les anciens highlights
        for item in self.graph_widget.scene.items():
            if hasattr(item, 'note_data') and hasattr(item, 'remove_highlight'):
                item.remove_highlight()

        matches = []
        for item in self.graph_widget.scene.items():
            if hasattr(item, 'note_data'):
                title = item.note_data.get("title", "").lower()
                if keyword in title:
                    matches.append(item)

        if not matches:
            print("❌ Aucune note trouvée avec ce mot-clé.")
            return

        for item in matches:
            item.highlight()

        if len(matches) == 1:
            self.graph_widget.centerOn(matches[0])
            self.graph_widget.resetTransform()
            self.graph_widget.scale(3, 3)
            print(f"🔍 Note unique trouvée et zoomée : {matches[0].note_data.get('title', '')}")
        else:
            print(f"🔍 {len(matches)} notes trouvées.")

    def keyPressEvent(self, event):
        """Gérer les raccourcis clavier (ex: Escape pour clear search, R pour recentrer)"""
        if event.key() == Qt.Key_Escape:
            if self.search_input.text().strip():  # 🆕 Vérifier si l'input n'est PAS vide
                self.on_reset_view_button_clicked()
                self.clear_search_highlights()
                print("🧹 Vue réinitialisée via Escape.")
        elif event.key() == Qt.Key_R:
            self.on_reset_view_button_clicked()
            print("🔄 Vue recentrée via touche R.")



    def clear_search_highlights(self):
        """Retirer tous les highlights de recherche et vider la barre de recherche"""
        for item in self.graph_widget.scene.items():
            if hasattr(item, 'remove_highlight'):
                item.remove_highlight()
        self.search_input.clear()  # 🆕 Vider la barre de recherche aussi

