from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QPainter
from PySide6.QtCore import Qt, QRectF, QPointF, QTimer
import json
from pathlib import Path
import math
import random
from collections import defaultdict

from app.components.note.modes.cluster.cluster_graph_interaction import TreeGraphInteraction
from app.components.note.modes.cluster.items.cluster_category_item import CategoryItem
from app.components.note.modes.cluster.items.cluster_note_item import NoteItem
from app.components.note.modes.cluster.cluster_camera_animation import animate_camera_to_center


class ClusterModeWidget(QGraphicsView):
    def __init__(self, notes_view, parent=None):
        super().__init__(parent)
        self.setObjectName("ClusterModeWidget")

        self.notes_view = notes_view

        self.interaction = TreeGraphInteraction(self)

        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setFrameStyle(QGraphicsView.NoFrame)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setViewportMargins(0, 0, 0, 0)
        self.setSceneRect(-100000, -100000, 200000, 200000)

        self.category_tree_path = Path("data/categories/category_tree.json")

        self.category_items = []
        self.note_items = []

        self.category_keyword_count = defaultdict(int)
        self.preload_note_keywords()

        self.timer = QTimer()
        self.timer.timeout.connect(self.advance_simulation)
        self.timer.start(16)

        self.scale(0.2, 0.2)
        self.centerOn(QPointF(0, 0))

        self.is_camera_animating = False

        self.init_graph()

    def init_graph(self):
        if not self.category_tree_path.exists():
            print("❌ category_tree.json non trouvé.")
            return

        with open(self.category_tree_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)

        self.center_pos = QPointF(0, 0)
        self.create_center_node(tree_data.get("name", "Cerveau"))

        for child in tree_data.get("children", []):
            self.add_category_recursively(child, self.center_pos)

        self.centerOn(self.center_pos)

        # ⏳ Initialisation différée des liens par mots-clés
        QTimer.singleShot(2000, self.init_keyword_links_for_all_notes)


    def create_center_node(self, label):
        radius = 80
        ellipse = QGraphicsEllipseItem(QRectF(-radius, -radius, radius * 2, radius * 2))
        ellipse.setBrush(QBrush(QColor("#EC831E")))
        ellipse.setPen(QPen(Qt.black, 3))
        ellipse.setZValue(1)
        self.scene.addItem(ellipse)

        text = QGraphicsTextItem(label)
        text.setDefaultTextColor(Qt.black)
        text.setZValue(2)
        text.setPos(-text.boundingRect().width() / 2, -text.boundingRect().height() / 2)
        self.scene.addItem(text)

    def add_category_recursively(self, node_data, origin_point, parent_item=None, depth=0, delay_ms=1000):
        def spawn_node():
            name = node_data["name"]
            children = node_data.get("children", [])
            notes = node_data.get("notes", [])
            num_children = len(children)

            item = CategoryItem(
                name=name,
                parent_ref=None if depth == 0 else parent_item,
                scene=self.scene,
                angle_hint=self.angle_from_origin(origin_point),
                num_children=num_children
            )
            self.category_items.append(item)

            # 🟡 Crée une liste pour stocker les notes liées à cette catégorie
            item.note_items = []

            # 🔵 Ajout des notes reliées à la catégorie
            for note_id in notes:
                note_item = NoteItem(
                    note_id=note_id,
                    parent_ref=item,
                    scene=self.scene,
                    notes_view=self.notes_view,
                    angle_hint=random.uniform(0, 2 * math.pi)
                )
                self.note_items.append(note_item)
                item.note_items.append(note_item)

            # 🔁 Ajout récursif des sous-catégories utiles uniquement
            for child_node in children:
                self.add_category_recursively(
                    child_node,
                    origin_point=item.pos_b,
                    parent_item=item,
                    depth=depth + 1,
                    delay_ms=delay_ms
                )

            self.update_category_display()

        QTimer.singleShot(depth * delay_ms, spawn_node)


    def angle_from_origin(self, point):
        if not point:
            return 0.0
        to_origin = QPointF(0, 0) - point
        return math.atan2(to_origin.y(), to_origin.x()) + math.pi

    def advance_simulation(self):
        for item in self.category_items:
            item.update_physics(other_items=self.category_items)
        for note in self.note_items:
            note.update_physics(other_notes=self.note_items)

    def update_category_display(self):
        current_zoom = self.transform().m11()
        for item in self.category_items:
            item.update_label_opacity(current_zoom)
            item.update_link_thickness(current_zoom)
            item.update_circle_outline_thickness(current_zoom)
            item.update_circle_visual_scale(current_zoom)
        for note in self.note_items:
            note.update_label_opacity(current_zoom)
            note.update_link_opacity(current_zoom)

    

    def preload_note_keywords(self):
        notes_dir = Path("data/notes")
        if not notes_dir.exists():
            return

        for note_file in notes_dir.glob("*.json"):
            try:
                with open(note_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    keywords = data.get("keywords", [])
                    for kw in keywords:
                        kw = kw.strip().lower()
                        self.category_keyword_count[kw] += 1
            except Exception as e:
                print(f"❌ Erreur lecture {note_file.name} : {e}")

    
    def get_selected_note_id(self):
        for note in self.note_items:
            if note.is_selected():
                return note.note_data.get("id")
        return None
    

    def add_note_live(self, note_id, keywords):
        for keyword in keywords:
            category_item = self.find_or_create_category_item(keyword)
            note_item = NoteItem(
                note_id=note_id,
                parent_ref=category_item,
                scene=self.scene,
                notes_view=self.notes_view,
                angle_hint=random.uniform(0, 2 * math.pi)
            )
            category_item.note_items.append(note_item)
            self.note_items.append(note_item)
            note_item.init_keyword_links(self.category_items)

        self.update_category_display()



    def find_or_create_category_item(self, keyword):
        for cat in self.category_items:
            if cat.name.lower() == keyword.lower():
                return cat

        # 🔧 Si non trouvé : créer une nouvelle catégorie visuelle
        from app.components.note.modes.cluster.items.cluster_category_item import CategoryItem

        item = CategoryItem(
            name=keyword,
            parent_ref=None,
            scene=self.scene,
            angle_hint=random.uniform(0, 2 * math.pi),
            num_children=0
        )
        item.note_items = []
        self.category_items.append(item)
        return item



    def delete_note_live(self, note_id):
        to_remove = None
        for note in self.note_items:
            if note.note_id == note_id:
                to_remove = note
                break

        if to_remove:
            self.scene.removeItem(to_remove.circle)
            self.scene.removeItem(to_remove.link)
            for _, link in to_remove.keyword_links:
                self.scene.removeItem(link)

            parent = to_remove.parent_ref
            if parent:
                parent.note_items.remove(to_remove)

            self.note_items.remove(to_remove)
            print(f"🗑️ Note visuelle supprimée : {note_id}")

            # 🔄 Vérifie si sa catégorie est vide
            if parent and not parent.note_items:
                self.scene.removeItem(parent.circle)
                self.scene.removeItem(parent.link)
                self.scene.removeItem(parent.label)
                self.category_items.remove(parent)
                print(f"🧹 Catégorie visuelle supprimée : {parent.name}")


        self.update_category_display()

        # 🔍 Charger les catégories valides depuis category_tree.json
        with open(self.category_tree_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)

        def collect_categories(node):
            names = set()
            if node["type"] == "category":
                names.add(node["name"].lower())
            for child in node.get("children", []):
                names.update(collect_categories(child))
            return names

        valid_categories = collect_categories(tree_data)

        # 🧹 Supprimer visuellement les catégories qui n’existent plus
        to_remove = []
        for cat in self.category_items:
            cat_name = cat.name.lower()
            if cat_name not in valid_categories:
                self.scene.removeItem(cat)
                to_remove.append(cat)
                print(f"🧹 Catégorie visuelle supprimée (hors JSON) : {cat_name}")

        for cat in to_remove:
            self.category_items.remove(cat)


    def reset_view(self):
        animate_camera_to_center(self)

    def refresh_selection_visual(self):
        for note in self.note_items:
            note.refresh_selection_state()






    def init_keyword_links_for_all_notes(self):
        for note in self.note_items:
            note.init_keyword_links(self.category_items)

    def wheelEvent(self, event):
        self.interaction.wheel_event(event)
        self.update_category_display()

    def mousePressEvent(self, event):
        self.interaction.mouse_press_event(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.interaction.mouse_move_event(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.interaction.mouse_release_event(event)
        super().mouseReleaseEvent(event)
