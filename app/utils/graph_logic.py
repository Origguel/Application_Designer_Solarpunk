import json
import math
import random
from pathlib import Path
from collections import defaultdict
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QColor, QPainterPath, QFont
from PySide6.QtCore import QPointF, QRectF, Qt

from app.components.interactive_ellipse_item import InteractiveEllipseItem  # 👈 LE BON IMPORT


NOTES_DIR = Path("data/notes/")

class GraphLogic:
    def __init__(self, graph_widget):
        self.widget = graph_widget
        self.scene = self.widget.scene

    def draw_graph(self):
        all_data = self.load_notes()
        positions, keyword_positions, keyword_links = self.calculate_positions(all_data)

        # Courbes entre catégories et notes
        for kw, pos in keyword_positions.items():
            for linked_kw in keyword_links.get(kw, []):
                if linked_kw in keyword_positions and linked_kw > kw:
                    self.draw_curve(pos, keyword_positions[linked_kw], QColor("lightgray"))
            for item in all_data:
                if kw in item.get("keywords", []) and item["id"] in positions:
                    self.draw_curve(pos, positions[item["id"]], QColor("gray"))

        # Nodes de notes
        for item in all_data:
            if item["id"] in positions:
                pos = positions[item["id"]]
                node_circle = InteractiveEllipseItem(QRectF(pos.x()-4, pos.y()-4, 8, 8), item, self.widget)
                node_circle.setData(0, item["id"])
                self.scene.addItem(node_circle)

                label = item["title"][:20] + ("..." if len(item["title"]) > 20 else "")
                text = self.scene.addText(f"{label}\n({item.get('type', '')})", QFont("Arial", 4))
                text.setDefaultTextColor(QColor("black"))
                text.setPos(pos.x() + 10, pos.y() - 10)
                self.widget.text_items.append(text)

        # Catégories
        for kw, pos in keyword_positions.items():
            self.scene.addEllipse(QRectF(pos.x()-8, pos.y()-8, 16, 16), QPen(Qt.black), Qt.white)
            text = self.scene.addText(kw.upper(), QFont("Arial", 8, QFont.Bold))
            text.setDefaultTextColor(QColor("black"))
            text.setPos(pos.x() + 12, pos.y() - 8)
            self.widget.text_items.append(text)

    def draw_curve(self, p1: QPointF, p2: QPointF, color):
        mid = (p1 + p2) / 2
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        ctrl = QPointF(mid.x() - dy/4, mid.y() + dx/4)
        path = QPainterPath(p1)
        path.quadTo(ctrl, p2)
        curve = QGraphicsPathItem(path)
        curve.setPen(QPen(color, 1))
        self.scene.addItem(curve)

    def load_notes(self):
        notes = []
        if NOTES_DIR.exists():
            for file in NOTES_DIR.glob("*.json"):
                with open(file, encoding="utf-8") as f:
                    notes.append(json.load(f))
        return notes

    def calculate_positions(self, all_data):
        keyword_counts = defaultdict(int)
        keyword_links = defaultdict(set)
        keyword_shared_notes = defaultdict(int)

        for item in all_data:
            for kw in item.get("keywords", []):
                keyword_counts[kw] += 1
            for i, kw1 in enumerate(item.get("keywords", [])):
                for kw2 in item.get("keywords", [])[i+1:]:
                    keyword_links[kw1].add(kw2)
                    keyword_links[kw2].add(kw1)
                    keyword_shared_notes[(kw1, kw2)] += 1
                    keyword_shared_notes[(kw2, kw1)] += 1

        valid_keywords = {k for k, c in keyword_counts.items() if c > 1}
        force_layout = {kw: QPointF(random.randint(-200, 200), random.randint(-200, 200)) for kw in valid_keywords}
        velocity = {kw: QPointF(0, 0) for kw in valid_keywords}

        for _ in range(150):
            for kw1 in valid_keywords:
                for kw2 in valid_keywords:
                    if kw1 == kw2:
                        continue
                    delta = force_layout[kw1] - force_layout[kw2]
                    distance = max(10, math.hypot(delta.x(), delta.y()))
                    repulsion = min(3000 / (distance ** 2), 400)
                    direction = delta / distance
                    velocity[kw1] += direction * repulsion

            for kw1 in valid_keywords:
                for kw2 in keyword_links.get(kw1, []):
                    if kw2 not in valid_keywords:
                        continue
                    delta = force_layout[kw2] - force_layout[kw1]
                    distance = max(10, math.hypot(delta.x(), delta.y()))
                    attraction = min(0.25 * (distance ** 2), 300)
                    direction = delta / distance
                    velocity[kw1] += direction * attraction

            for kw in valid_keywords:
                velocity[kw] *= 0.75
                force_layout[kw] += velocity[kw]

        keyword_positions = {kw: pos for kw, pos in force_layout.items()}

        positions = {}
        for item in all_data:
            keywords = [kw for kw in item.get("keywords", []) if kw in keyword_positions]
            if keywords:
                avg_x = sum(keyword_positions[kw].x() for kw in keywords) / len(keywords)
                avg_y = sum(keyword_positions[kw].y() for kw in keywords) / len(keywords)
                jitter_x = random.uniform(-20, 20)
                jitter_y = random.uniform(-20, 20)
                positions[item["id"]] = QPointF(avg_x + jitter_x, avg_y + jitter_y)

        return positions, keyword_positions, keyword_links

    def update_text_visibility(self):
        scale = self.widget.transform().m11()
        for item in self.widget.text_items:
            item.setVisible(scale > 1.5)
