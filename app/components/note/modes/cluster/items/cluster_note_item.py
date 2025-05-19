from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QFont
from PySide6.QtCore import QPointF, Qt
import math
import random
import json
from pathlib import Path

from app.components.note.modes.cluster.items.cluster_interactive_note_circle_item import InteractiveNoteCircleItem
from app.utils.note_selection_manager import get_selected_note_id

class NoteItem(QGraphicsItem):
    MIN_ZOOM = 0.6
    MAX_ZOOM = 0.8

    def __init__(self, note_id, parent_ref, scene, notes_view, radius=8, base_distance=150, angle_hint=None):
        super().__init__()
        self.note_id = note_id
        self.parent_ref = parent_ref
        self.scene = scene
        self.notes_view = notes_view
        self.radius = radius
        self.distance = base_distance
        self.safe_distance = 5
        self.velocity = QPointF(0, 0)
        self.keyword_links = []
        self._selected = False
        self._highlighted = False

        self.angle = angle_hint + random.uniform(-0.3, 0.3) if angle_hint else random.uniform(0, 2 * math.pi)
        r = self.distance * random.uniform(0.6, 0.9)
        self.pos_b = self.origin() + QPointF(r * math.cos(self.angle), r * math.sin(self.angle))

        self.load_note_data()
        self.create_main_link()
        self.create_circle_item()
        self.create_label()

    # ---------- Chargement des données ----------

    def load_note_data(self):
        note_path = Path(f"data/notes/{self.note_id}.json")
        if note_path.exists():
            with open(note_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {"id": self.note_id}

    # ---------- Création des éléments visuels ----------

    def create_main_link(self):
        self.link = QGraphicsLineItem()
        self.link.setPen(QPen(Qt.black, 1.5))
        self.scene.addItem(self.link)

    def create_circle_item(self):
        self.circle = InteractiveNoteCircleItem(self.note_id, self.notes_view)
        self.circle.setParentItem(self)
        self.circle.setRect(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
        self.circle.setBrush(QBrush(Qt.black))
        self.circle.setPen(QPen(Qt.transparent))
        self.circle.setZValue(1)
        self.circle.note = self
        self.scene.addItem(self.circle)

    def create_label(self):
        title = self.data.get("title", self.note_id)
        if len(title) > 24:
            title = title[:21] + "..."
        self.label = QGraphicsTextItem(title)
        self.label.setDefaultTextColor(Qt.black)
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setZValue(4)
        self.label.setParentItem(self.circle)
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, -self.radius - rect.height() - 2)

    # ---------- Sélection & Style ----------

    def refresh_selection_state(self):
        self.set_selected(get_selected_note_id() == self.note_id)

    def set_selected(self, state):
        self._selected = state
        self.circle.setScale(2.0 if state else 1.0)
        self.label.setScale(1.4 if state else 1.0)
        self.update_visual_style()

    def is_selected(self):
        return self._selected

    def highlight(self):
        self._highlighted = True
        self.update_visual_style()

    def remove_highlight(self):
        self._highlighted = False
        self.update_visual_style()

    def update_visual_style(self):
        if self._selected:
            self.circle.setBrush(QBrush(QColor("#F18805")))
            self.circle.setPen(QPen(Qt.transparent))
        elif self._highlighted:
            self.circle.setBrush(QBrush(QColor("#F4B67C")))
            self.circle.setPen(QPen(Qt.transparent))
        else:
            self.circle.setBrush(QBrush(Qt.black))
            self.circle.setPen(QPen(Qt.transparent))

    # ---------- Physique & Simulation ----------

    def origin(self):
        return self.parent_ref.pos_b if self.parent_ref else QPointF(0, 0)

    def add_to_velocity(self, dx, dy):
        self.velocity += QPointF(dx, dy)

    def update_physics(self, other_notes=[], friction=0.8, velocity_strenght=0.05):
        dx = self.pos_b.x() - self.origin().x()
        dy = self.pos_b.y() - self.origin().y()
        dist = math.hypot(dx, dy)
        if dist != 0:
            factor = (self.distance - dist) / dist
            self.add_to_velocity(dx * factor * velocity_strenght, dy * factor * velocity_strenght)

        base_repel = 200 / math.sqrt(max(1, len(getattr(self.parent_ref, "note_items", []))))
        for other in other_notes:
            if other is self:
                continue
            delta = self.pos_b - other.pos_b
            dist = max(1, math.hypot(delta.x(), delta.y()))
            if dist < self.radius * self.safe_distance:
                force = base_repel * ((1 - dist / (self.radius * self.safe_distance)) ** 2)
                self.add_to_velocity(delta.x() / dist * force, delta.y() / dist * force)

        for category, _ in self.keyword_links:
            delta = category.pos_b - self.pos_b
            dist = math.hypot(delta.x(), delta.y())
            if dist > 1:
                self.add_to_velocity(delta.x() / dist * 0.4, delta.y() / dist * 0.4)

        self.velocity *= friction
        self.pos_b += self.velocity

        self.circle.setPos(self.pos_b)
        self.link.setLine(self.origin().x(), self.origin().y(), self.pos_b.x(), self.pos_b.y())

        for category, link in self.keyword_links:
            link.setLine(self.pos_b.x(), self.pos_b.y(), category.pos_b.x(), category.pos_b.y())

    # ---------- Liens et mots-clés ----------

    def init_keyword_links(self, all_categories):
        note_path = Path(f"data/notes/{self.note_id}.json")
        if not note_path.exists():
            return
        with open(note_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        keywords = [kw.lower() for kw in data.get("keywords", [])]
        self.keyword_links.clear()

        for category in all_categories:
            if category.name.lower() in keywords:
                link = QGraphicsLineItem()
                pen = QPen(QColor("#D5D5D5"))
                pen.setWidthF(1.0)
                link.setPen(pen)
                link.setZValue(0)
                self.scene.addItem(link)
                self.keyword_links.append((category, link))

        self.distance = 200 + len(self.keyword_links) * 100

    # ---------- Zoom et Opacité ----------

    def update_label_opacity(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        self.label.setOpacity((zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM))

    def update_link_opacity(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        opacity = 1.0 - (0.8 * ((zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)))

        for _, link in self.keyword_links:
            color = link.pen().color()
            color.setAlphaF(opacity)
            pen = link.pen()
            pen.setColor(color)
            link.setPen(pen)

        color = self.link.pen().color()
        color.setAlphaF(opacity)
        pen = self.link.pen()
        pen.setColor(color)
        self.link.setPen(pen)

    # ---------- Divers ----------

    def boundingRect(self):
        return self.circle.mapRectToParent(self.circle.rect())