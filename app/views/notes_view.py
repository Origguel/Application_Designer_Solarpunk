# app/views/notes_view.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtWidgets import QLineEdit
import json
from pathlib import Path

from app.components.note.graph.graph_widget import GraphWidget
from app.components.note.add_note_widget import AddNoteWidget
from app.handlers.delete_note_handler import confirm_and_delete_note
from app.components.note.graph.interactive_ellipse_item import InteractiveEllipseItem
from app.utils.categorie_manager.category_manager import CategoryManager
from app.components.note.graph.tree_graph_widget import TreeGraphWidget
from app.components.note.graph.note_detail_widget import NoteDetailWidget


# Componenents
from app.components.inputs.input_default import Input_Default
from app.components.buttons.button_icon import ButtonIcon



class NotesView(QWidget):
    def __init__(self):
        super().__init__()

        self.is_camera_animating = False

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Graph principal
        self.graph_widget = TreeGraphWidget(self)
        self.layout.addWidget(self.graph_widget)
        self.graph_widget.scale(0.2, 0.2)

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
        self.search_input = Input_Default(placeholder="Rechercher une note...", x=400, y=36, text_position="center-left", parent=self)
        self.search_input.move(74, 26)
        self.search_input.raise_()
        self.search_input.textChanged.connect(self.on_search_note)


        # Panneau d'ajout
        self.add_note_widget = None

    def open_note_detail(self, note_id):
        """Affiche le détail d'une note dans un panneau à droite"""
        note_path = Path(f"data/notes/{note_id}.json")
        if not note_path.exists():
            print(f"❌ Fichier de note introuvable : {note_path}")
            return

        with open(note_path, "r", encoding="utf-8") as f:
            note_data = json.load(f)

        self.close_note_detail()  # ✅ remplacement sécurisé

        self.note_detail_widget = NoteDetailWidget(note_data, self)
        widget_width = 460
        top_margin = 68
        right_margin = 34
        bottom_margin = 26
        available_height = self.height() - top_margin - bottom_margin

        self.note_detail_widget.setGeometry(
            self.width() - widget_width - right_margin,
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
        if selected_note_id:
            confirm_and_delete_note(self, selected_note_id)
            CategoryManager().update()  # 🆕 Mise à jour après suppression
            self.refresh_graph()        # 🆕 Redessiner le graphe


    def on_reset_view_button_clicked(self):
        if self.is_camera_animating:
            print("⏳ Animation déjà en cours.")
            return

        current_center = self.graph_widget.mapToScene(self.graph_widget.viewport().rect().center())
        current_scale = self.graph_widget.transform().m11()

        center_threshold = 5.0
        scale_threshold = 0.01
        target_center = QPointF(0, 0)
        target_scale = 0.1

        if (current_center - target_center).manhattanLength() < center_threshold and abs(current_scale - target_scale) < scale_threshold:
            print("✅ Vue déjà centrée et zoomée, animation ignorée.")
            return

        self.animate_camera_to_center()



    def on_search_note(self):
        """Handler appelé quand on valide une recherche"""
        keyword = self.search_input.text().strip().lower()

        if not keyword:
            self.clear_search_highlights()
            return

        # D'abord, retirer tous les anciens highlights
        for item in self.graph_widget.scene.items():
            if hasattr(item, 'note_data') and hasattr(item, 'remove_highlight'):
                item.remove_highlight()

        matches = []
        for item in self.graph_widget.category_items + self.graph_widget.note_items:
            if hasattr(item, 'note_data'):
                title = item.note_data.get("title", "").lower()
                words = title.split()
                if keyword in words:
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
            self.clear_search_highlights()
            self.on_reset_view_button_clicked()
            print("🧹 Vue réinitialisée via Escape.")
        elif event.key() == Qt.Key_R:
            self.on_reset_view_button_clicked()
            print("🔄 Vue recentrée via touche R.")



    def clear_search_highlights(self):
        """Retirer tous les highlights de recherche et vider la barre de recherche"""
        for item in self.graph_widget.note_items:
            if hasattr(item, 'remove_highlight'):
                item.remove_highlight()
        self.search_input.clear()
        self.graph_widget.update_category_display()

    from PySide6.QtCore import QTimer, QPointF

    def animate_camera_to_center(self, duration_ms=1000, target_scale=0.1):
        def ease_in_out_expo(t):
            if t == 0:
                return 0
            if t == 1:
                return 1
            if t < 0.5:
                return 0.5 * pow(2, 20 * t - 10)
            else:
                return 1 - 0.5 * pow(2, -20 * t + 10)

        if self.is_camera_animating:
            return

        view = self.graph_widget
        self.is_camera_animating = True
        view.setInteractive(False)  # 🛑 désactive les interactions

        steps = 60
        interval = duration_ms // steps
        initial_scale = view.transform().m11()
        scale_diff = target_scale - initial_scale
        current_center = view.mapToScene(view.viewport().rect().center())
        target_center = QPointF(0, 0)
        delta_center = target_center - current_center
        step = 0

        def animate_step():
            nonlocal step
            if step >= steps:
                timer.stop()
                view.setInteractive(True)
                self.is_camera_animating = False
                print("✅ Animation terminée")
                return

            t = ease_in_out_expo((step + 1) / steps)
            interpolated_scale = initial_scale + scale_diff * t
            interpolated_center = current_center + delta_center * t

            view.resetTransform()
            view.scale(interpolated_scale, interpolated_scale)
            view.centerOn(interpolated_center)
            self.graph_widget.update_category_display()

            step += 1

        timer = QTimer(self)
        timer.timeout.connect(animate_step)
        timer.start(interval)
