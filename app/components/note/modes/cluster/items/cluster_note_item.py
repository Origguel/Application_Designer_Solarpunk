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
        self.radius = radius
        self.scene = scene
        self.distance = base_distance
        self.safe_distance = 5
        self.velocity = QPointF(0, 0)
        self.keyword_links = []  # 🔗 liens visuels vers catégories par mot-clé

        self._highlighted = False

        # Position initiale
        self.angle = angle_hint + random.uniform(-0.3, 0.3) if angle_hint else random.uniform(0, 2 * math.pi)
        r = self.distance * random.uniform(0.6, 0.9)
        self.pos_b = self.origin() + QPointF(r * math.cos(self.angle), r * math.sin(self.angle))

        # Lien principal vers la catégorie d’origine
        self.link = QGraphicsLineItem()
        self.link.setPen(QPen(Qt.black, 1.5))  # Lien direct bien visible
        scene.addItem(self.link)

        # Cercle noir (sans bordure)
        self.circle = InteractiveNoteCircleItem(self.note_id, notes_view)
        self.circle.setParentItem(self)
        self.circle.setRect(-radius, -radius, radius * 2, radius * 2)
        self.circle.setBrush(QBrush(Qt.black))
        self.circle.setPen(QPen(Qt.transparent))
        self.circle.setZValue(1)
        scene.addItem(self.circle)

        self._selected = False
        self.circle.note = self  # ✅ clé de la communication

        note_path = Path(f"data/notes/{note_id}.json")
        if note_path.exists():
            with open(note_path, "r", encoding="utf-8") as f:
                self.note_data = json.load(f)
            MAX_LABEL_LENGTH = 24
            note_title = self.note_data.get("title", note_id)
            if len(note_title) > MAX_LABEL_LENGTH:
                note_title = note_title[:MAX_LABEL_LENGTH - 3] + "…"
        else:
            self.note_data = {"id": note_id}
            note_title = note_id

        # Titre de la note (affiché au-dessus du point)
        self.label = QGraphicsTextItem(note_title)
        self.label.setDefaultTextColor(Qt.black)
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setZValue(4)
        self.label.setParentItem(self.circle)
        text_rect = self.label.boundingRect()
        self.label.setPos(-text_rect.width() / 2, -self.radius - text_rect.height() - 2)
        
        

    def origin(self):
        return self.parent_ref.pos_b if self.parent_ref else QPointF(0, 0)

    def add_to_velocity(self, dx, dy):
        self.velocity = QPointF(self.velocity.x() + dx, self.velocity.y() + dy)

    def load_keywords_and_links(self, all_categories):
        note_path = Path(f"data/notes/{self.note_id}.json")
        if not note_path.exists():
            print(f"❌ Note JSON non trouvé : {note_path}")
            return

        with open(note_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        keywords = [kw.lower() for kw in data.get("keywords", [])]

        # Cherche des catégories liées par mot-clé
        for category in all_categories:
            cat_name = category.name.lower()
            if cat_name in keywords:
                visual_link = QGraphicsLineItem()
                visual_link.setPen(QPen(QColor("#AAAAAA"), 0.5, Qt.DashLine))
                visual_link.setZValue(0)
                self.scene.addItem(visual_link)
                self.keyword_links.append((category, visual_link))

    def update_physics(self, other_notes=[], friction=0.8, velocity_strenght=0.05):
        dx = self.pos_b.x() - self.origin().x()
        dy = self.pos_b.y() - self.origin().y()
        current_dist = math.hypot(dx, dy)
        if current_dist != 0:
            factor = (self.distance - current_dist) / current_dist
            self.add_to_velocity(dx * factor * velocity_strenght, dy * factor * velocity_strenght)

        # Repoussement avec force adaptative
        base_repel_strength = 200
        note_count = len(getattr(self.parent_ref, "note_items", []))
        note_count = max(note_count, 1)
        repel_strength = base_repel_strength / math.sqrt(note_count)

        for other in other_notes:
            if other is self:
                continue
            delta = self.pos_b - other.pos_b
            dist = math.hypot(delta.x(), delta.y())
            if dist < 1:
                dist = 1
            if dist < self.radius * self.safe_distance:
                force_factor = 1 - (dist / (self.radius * self.safe_distance))
                repel_force = repel_strength * (force_factor ** 2)
                self.add_to_velocity(
                    delta.x() / dist * repel_force,
                    delta.y() / dist * repel_force
                )

        # 🔄 Attirance vers les catégories liées par mots-clés
        attract_strength = 0.4  # plus bas = plus doux
        for category, _ in self.keyword_links:
            delta = category.pos_b - self.pos_b
            dist = math.hypot(delta.x(), delta.y())
            if dist > 1:
                self.add_to_velocity(
                    delta.x() / dist * attract_strength,
                    delta.y() / dist * attract_strength
                )


        self.velocity *= friction
        self.pos_b += self.velocity

        self.circle.setPos(self.pos_b)
        self.link.setLine(self.origin().x(), self.origin().y(), self.pos_b.x(), self.pos_b.y())

        # 🔁 Met à jour les liens visuels vers les catégories correspondantes aux mots-clés
        for category, link in self.keyword_links:
            link.setLine(self.pos_b.x(), self.pos_b.y(), category.pos_b.x(), category.pos_b.y())


    def init_keyword_links(self, all_categories):
        note_path = Path(f"data/notes/{self.note_id}.json")
        if not note_path.exists():
            print(f"❌ Note JSON non trouvé : {note_path}")
            return

        with open(note_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        keywords = [kw.lower() for kw in data.get("keywords", [])]
        self.keyword_links = []

        for category in all_categories:
            if category.name.lower() in keywords:
                visual_link = QGraphicsLineItem()
                pen = QPen(QColor("#D5D5D5"))
                pen.setWidthF(1.0)
                pen.setStyle(Qt.SolidLine)
                visual_link.setZValue(0)
                self.scene.addItem(visual_link)
                self.keyword_links.append((category, visual_link))

        # 🧠 Distance adaptative en fonction du nombre de catégories liées
        num_links = len(self.keyword_links)
        base = 200
        increment = 100
        self.distance = base + (num_links * increment)


    def update_label_opacity(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        normalized = (zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)
        self.label.setOpacity(normalized)

    def update_link_opacity(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        normalized = (zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)

        # Inverser la courbe : plus on zoom, plus c’est transparent
        opacity = 1.0 - (0.8 * normalized)  # de 1.0 à 0.4

        # 🔁 Appliquer à tous les liens secondaires
        for _, link in self.keyword_links:
            color = link.pen().color()
            color.setAlphaF(opacity)
            pen = link.pen()
            pen.setColor(color)
            link.setPen(pen)

        # ✅ Appliquer au lien principal
        main_color = self.link.pen().color()
        main_color.setAlphaF(opacity)
        main_pen = self.link.pen()
        main_pen.setColor(main_color)
        self.link.setPen(main_pen)

    def is_highlighted(self):
        return self._highlighted

    def highlight(self):
        self._highlighted = True
        self.circle.setBrush(QBrush(QColor("#F18805")))  # Orange intérieur
        self.circle.setPen(QPen(Qt.black, 1.5))          # Bordure noire


    def remove_highlight(self):
        self._highlighted = False
        self.refresh_brush()


    def refresh_brush(self):
        if self._selected:
            self.circle.setBrush(QBrush(QColor("#F18805")))  # Orange plein
            self.circle.setPen(QPen(Qt.transparent))          # Pas de bordure
        elif self._highlighted:
            self.circle.setBrush(QBrush(QColor("#F18805")))   # Orange clair
            self.circle.setPen(QPen(Qt.black, 1.5))           # Bordure noire fine
        else:
            self.circle.setBrush(QBrush(Qt.black))            # Cercle noir
            self.circle.setPen(QPen(Qt.transparent))          # Pas de bordure



    def select(self):
        self._selected = True
        self.circle.setScale(2.0)
        self.label.setScale(1.4)
        self.circle.setBrush(QBrush(QColor("#F18805")))  # Orange sélection
        self.refresh_brush()

    def deselect(self):
        self._selected = False
        self.circle.setScale(1.0)
        self.label.setScale(1.0)
        self.refresh_brush()

    def boundingRect(self):
        return self.circle.mapRectToParent(self.circle.rect())
    
    def is_selected(self):
        return self._selected
    
    def refresh_selection_state(self):
        selected_id = get_selected_note_id()
        if self.note_id == selected_id:
            self.select()
        else:
            self.deselect()