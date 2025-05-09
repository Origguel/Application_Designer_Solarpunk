from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QPainter
from PySide6.QtCore import Qt, QRectF, QPointF, QTimer
import json
from pathlib import Path

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
        """Ajoute une catégorie connectée à un point donné (le centre ou une autre catégorie)"""
        item = CategoryItem(name=name, origin_point=origin_point, scene=self.scene)
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
        """Ajoute une catégorie après un délai, puis ses enfants avec délai décalé"""
        def spawn_node():
            name = node_data["name"]
            item = CategoryItem(name=name, origin_point=origin_point, scene=self.scene)
            self.category_items.append(item)

            # Ajouter les enfants avec +1 niveau
            for child_node in node_data.get("children", []):
                self.add_category_recursively(child_node, item.pos_b, depth=depth + 1)

        # Lancer l'ajout après un délai
        QTimer.singleShot(depth * delay_ms, spawn_node)







    

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
