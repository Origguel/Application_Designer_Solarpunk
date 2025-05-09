from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QPainter
from PySide6.QtCore import Qt, QRectF, QPointF, QTimer
import json
from pathlib import Path
import math

from app.utils.tree_graph_interaction import TreeGraphInteraction
from app.components.note.graph.category_item import CategoryItem


class TreeGraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interaction = TreeGraphInteraction(self)

        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.category_tree_path = Path("data/categories/category_tree.json")

        # Simulation
        self.category_items = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.advance_simulation)
        self.timer.start(16)  # Environ 60 FPS

        self.init_graph()

    def init_graph(self):
        """Charge le JSON et place le centre + catégories"""
        if not self.category_tree_path.exists():
            print("❌ category_tree.json non trouvé.")
            return

        with open(self.category_tree_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)

        self.center_pos = QPointF(0, 0)
        self.create_center_node(tree_data.get("name", "Cerveau"))

        for child in tree_data.get("children", []):
            self.add_category(child["name"], self.center_pos)

        self.centerOn(self.center_pos)

    def create_center_node(self, label):
        """Crée le centre du graphe : le cerveau"""
        radius = 80
        ellipse = QGraphicsEllipseItem(QRectF(-radius, -radius, radius * 2, radius * 2))
        ellipse.setBrush(QBrush(QColor("orange")))
        ellipse.setPen(QPen(Qt.black, 3))
        ellipse.setZValue(1)
        self.scene.addItem(ellipse)

        text = QGraphicsTextItem(label)
        text.setDefaultTextColor(Qt.black)
        text.setZValue(2)
        text.setPos(-text.boundingRect().width() / 2, -text.boundingRect().height() / 2)
        self.scene.addItem(text)

    def add_category(self, name, origin_point):
        distance = 800  # ou une valeur fixe par défaut
        angle = self.angle_from_origin(origin_point)
        item = CategoryItem(name=name, origin_point=origin_point, scene=self.scene, distance=distance, angle_hint=angle)
        self.category_items.append(item)


    def advance_simulation(self):
        """Met à jour la position de chaque catégorie"""
        for item in self.category_items:
            item.update_physics(other_items=self.category_items)

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

    def add_category_recursively(self, node_data, origin_point, depth=0, delay_ms=4000):
        """Ajoute une catégorie après un délai, avec une distance adaptée au nombre d'enfants"""
        def spawn_node():
            name = node_data["name"]
            children = node_data.get("children", [])
            num_children = len(children)

            # Distance en fonction du nombre d’enfants et profondeur
            base_distance = 500
            distance = base_distance + (num_children * 300) + (depth * 150)
            distance = min(max(distance, 300), 2000)  # clamp entre 300 et 1800 px

            item = CategoryItem(
                name=name,
                origin_point=origin_point,
                scene=self.scene,
                distance=distance,
                angle_hint=self.angle_from_origin(origin_point),
                num_children=num_children  # 🧠 transmis ici
            )

            self.category_items.append(item)

            for child_node in children:
                self.add_category_recursively(child_node, item.pos_b, depth=depth + 1, delay_ms=delay_ms)

        QTimer.singleShot(depth * delay_ms, spawn_node)


    def angle_from_origin(self, point):
        if not point:
            return 0.0
        to_origin = QPointF(0, 0) - point
        return math.atan2(to_origin.y(), to_origin.x()) + math.pi







    

    def wheelEvent(self, event):
        self.interaction.wheel_event(event)

    def mousePressEvent(self, event):
        self.interaction.mouse_press_event(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.interaction.mouse_move_event(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.interaction.mouse_release_event(event)
        super().mouseReleaseEvent(event)
