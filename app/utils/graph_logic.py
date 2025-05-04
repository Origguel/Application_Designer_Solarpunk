import json
import math
import random
from pathlib import Path
from collections import defaultdict, deque
from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtGui import QPen, QColor, QFont
from PySide6.QtCore import QPointF, QRectF, Qt

from app.components.note.graph.interactive_ellipse_item import InteractiveEllipseItem

NOTES_DIR = Path("data/notes/")

# ===== CONFIGURATION =====

# --- Zoom thresholds (affichage progressif selon le niveau de zoom) ---
ZOOM_FAR = 0.4        # Zoom minimal pour afficher les notes
ZOOM_MEDIUM = 0.7     # Zoom pour afficher les titres de catégories
ZOOM_CLOSE = 2.4      # Zoom pour afficher les titres de notes

# --- Seuils pour filtrer les catégories et les liens entre elles ---
MIN_NOTE_PER_CATEGORY = 5     # Nombre minimal de notes pour qu’un mot-clé soit une "catégorie"
MIN_LINK_BETWEEN_CATEGORIES = 1  # Nombre minimal de cooccurrences entre deux catégories pour qu’un lien soit créé

# --- Paramètres pour la force de répulsion/attraction dans le layout ---
REPULSION_BASE = 30           # Distance de répulsion minimale
REPULSION_PER_NOTE = 10       # Répulsion supplémentaire par note liée à la catégorie
CATEGORY_ATTRACTION = 0.01    # Force d’attraction entre catégories liées
CATEGORY_REPULSION_FORCE = 0.2  # Force de répulsion si trop proches
CATEGORY_ITERATIONS = 200     # Nombre d’itérations de la simulation

# --- Positionnement des notes orphelines ---
ORPHAN_RADIUS = 1200          # Distance par rapport au centre
ORPHAN_JITTER = 50            # Jitter aléatoire autour de leur cercle
# ==============================


class GraphLogic:
    def __init__(self, graph_widget):
        self.widget = graph_widget
        self.scene = self.widget.scene
        self.widget.text_items = []
        self.widget.note_items = []
        self.widget.link_items = []
        self.widget.cat_text_items = []
        self.widget.cat_link_items = []

    def draw_graph(self):
        all_data = self.load_notes()
        category_positions, category_links = self.calculate_category_positions(all_data)

        # Lien entre catégories
        for cat1, linked in category_links.items():
            for cat2 in linked:
                if cat1 < cat2:
                    p1 = category_positions[cat1]
                    p2 = category_positions[cat2]
                    line = QGraphicsLineItem(p1.x(), p1.y(), p2.x(), p2.y())
                    pen = QPen(QColor("black"), 2)
                    line.setPen(pen)
                    line.setZValue(-2)
                    self.scene.addItem(line)
                    self.widget.cat_link_items.append(line)

        # Dessiner les catégories
        for cat, pos in category_positions.items():
            self.scene.addEllipse(QRectF(pos.x() - 10, pos.y() - 10, 20, 20), QPen(Qt.black, 2), Qt.white)
            text = self.scene.addText(cat.upper(), QFont("Arial", 8, QFont.Bold))
            text.setDefaultTextColor(QColor("black"))
            text.setZValue(1)
            text.setPos(pos.x() + 12, pos.y() - 8)
            self.widget.cat_text_items.append(text)

        # Dessiner les notes
        for note in all_data:
            keywords = [kw for kw in note.get("keywords", []) if kw in category_positions]
            if not keywords:
                continue

            def category_weight(kw):
                return len(category_links[kw])

            sorted_keywords = sorted(keywords, key=category_weight, reverse=True)
            primary_kw = sorted_keywords[0]
            base_pos = category_positions[primary_kw]

            offset = QPointF(0, 0)
            for kw in sorted_keywords[1:]:
                direction = category_positions[kw] - base_pos
                offset += direction * 0.25

            jitter = QPointF(random.uniform(-20, 20), random.uniform(-20, 20))
            angle = random.uniform(0, 2 * math.pi)
            radius = 60 + 15 * len(keywords)
            spread = QPointF(math.cos(angle) * radius, math.sin(angle) * radius)

            final_pos = base_pos + offset + spread + jitter

            ellipse = InteractiveEllipseItem(QRectF(final_pos.x() - 4, final_pos.y() - 4, 8, 8), note, self.widget)
            ellipse.setData(0, note["id"])
            ellipse.setZValue(0)
            self.scene.addItem(ellipse)
            self.widget.note_items.append(ellipse)

            label = note["title"][:20] + ("..." if len(note["title"]) > 20 else "")
            text = self.scene.addText(f"{label}\n({note.get('type', '')})", QFont("Arial", 4))
            text.setDefaultTextColor(QColor("black"))
            text.setZValue(1)
            text.setPos(final_pos.x() + 6, final_pos.y() - 6)
            self.widget.text_items.append(text)

            for kw in keywords:
                kw_pos = category_positions[kw]
                link = QGraphicsLineItem(final_pos.x(), final_pos.y(), kw_pos.x(), kw_pos.y())
                link.setPen(QPen(QColor("gray"), 1))
                link.setZValue(-1)
                self.scene.addItem(link)
                self.widget.link_items.append(link)


                # === NOTES ORPHELINES ===
        orphan_notes = [note for note in all_data if not any(kw in category_positions for kw in note.get("keywords", []))]
        if orphan_notes:
            # Centrer autour du barycentre des catégories
            all_cat_pos = list(category_positions.values())
            if all_cat_pos:
                center = sum(all_cat_pos, QPointF(0, 0)) / len(all_cat_pos)
            else:
                center = QPointF(0, 0)

            count = len(orphan_notes)
            for i, note in enumerate(orphan_notes):
                angle = 2 * math.pi * i / count
                x = center.x() + math.cos(angle) * ORPHAN_RADIUS + random.uniform(-ORPHAN_JITTER, ORPHAN_JITTER)
                y = center.y() + math.sin(angle) * radius + random.uniform(-50, 50)
                pos = QPointF(x, y)

                ellipse = InteractiveEllipseItem(QRectF(pos.x() - 4, pos.y() - 4, 8, 8), note, self.widget)
                ellipse.setData(0, note["id"])
                ellipse.setZValue(0)
                self.scene.addItem(ellipse)
                self.widget.note_items.append(ellipse)

                label = note["title"][:20] + ("..." if len(note["title"]) > 20 else "")
                text = self.scene.addText(f"{label}\n({note.get('type', '')})", QFont("Arial", 4))
                text.setDefaultTextColor(QColor("black"))
                text.setZValue(1)
                text.setPos(pos.x() + 6, pos.y() - 6)
                self.widget.text_items.append(text)


    def load_notes(self):
        notes = []
        if NOTES_DIR.exists():
            for file in NOTES_DIR.glob("*.json"):
                with open(file, encoding="utf-8") as f:
                    notes.append(json.load(f))
        return notes

    def calculate_category_positions(self, all_data):
        keyword_counts = defaultdict(int)
        keyword_pair_counts = defaultdict(int)
        keyword_to_notes = defaultdict(set)

        for note in all_data:
            kws = note.get("keywords", [])
            for kw in kws:
                keyword_counts[kw] += 1
                keyword_to_notes[kw].add(note["id"])
            for i, kw1 in enumerate(kws):
                for kw2 in kws[i + 1:]:
                    key = tuple(sorted((kw1, kw2)))
                    keyword_pair_counts[key] += 1

        valid_categories = {kw for kw, count in keyword_counts.items() if count >= MIN_NOTE_PER_CATEGORY}

        links = defaultdict(set)
        for (kw1, kw2), count in keyword_pair_counts.items():
            if kw1 in valid_categories and kw2 in valid_categories and count >= MIN_LINK_BETWEEN_CATEGORIES:
                links[kw1].add(kw2)
                links[kw2].add(kw1)

        repulsion_radius = {
            kw: REPULSION_BASE + REPULSION_PER_NOTE * len(keyword_to_notes[kw])
            for kw in valid_categories
        }

        def hash_seed(key): return hash(key) & 0xffffffff

        def get_connected_components(graph):
            visited = set()
            components = []
            for node in graph:
                if node not in visited:
                    queue = deque([node])
                    group = set()
                    while queue:
                        current = queue.popleft()
                        if current not in visited:
                            visited.add(current)
                            group.add(current)
                            queue.extend(graph[current])
                    components.append(group)
            return components

        components = get_connected_components(links)
        global_positions = {}

        cols = math.ceil(math.sqrt(len(components)))
        spacing = 800
        random_offset = random.Random(42)

        for i, group in enumerate(components):
            group = list(group)
            rnd = random.Random(i)
            local_pos = {
                kw: QPointF(rnd.uniform(-100, 100), rnd.uniform(-100, 100))
                for kw in group
            }
            velocity = {kw: QPointF(0, 0) for kw in group}

            for _ in range(CATEGORY_ITERATIONS):
                for kw1 in group:
                    for kw2 in group:
                        if kw1 == kw2:
                            continue
                        delta = local_pos[kw1] - local_pos[kw2]
                        dist = max(1, math.hypot(delta.x(), delta.y()))
                        min_dist = repulsion_radius[kw1] + repulsion_radius[kw2]
                        if dist < min_dist:
                            direction = delta / dist
                            force = CATEGORY_REPULSION_FORCE * (min_dist - dist)
                            velocity[kw1] += direction * force

                for kw1 in group:
                    for kw2 in links[kw1]:
                        if kw2 not in group:
                            continue
                        delta = local_pos[kw2] - local_pos[kw1]
                        dist = max(10, math.hypot(delta.x(), delta.y()))
                        direction = delta / dist
                        attraction = CATEGORY_ATTRACTION * dist
                        velocity[kw1] += direction * attraction

                for kw in group:
                    velocity[kw] *= 0.7
                    local_pos[kw] += velocity[kw]

            row = i // cols
            col = i % cols
            base_x = col * spacing
            base_y = row * spacing
            jitter_x = random_offset.uniform(-150, 150)
            jitter_y = random_offset.uniform(-150, 150)
            offset = QPointF(base_x + jitter_x, base_y + jitter_y)

            for kw in group:
                global_positions[kw] = local_pos[kw] + offset

        return global_positions, links

    def update_text_visibility(self):
        scale = self.widget.transform().m11()

        def interpolate(a, b, t):
            return a + (b - a) * t

        def clamp(x, minimum, maximum):
            return max(minimum, min(x, maximum))

        # Texte des notes
        for text in self.widget.text_items:
            if text is not None:
                if scale < ZOOM_MEDIUM:
                    text.setOpacity(0)
                elif scale > ZOOM_CLOSE:
                    text.setOpacity(1)
                else:
                    t = (scale - ZOOM_MEDIUM) / (ZOOM_CLOSE - ZOOM_MEDIUM)
                    text.setOpacity(clamp(t, 0, 1))

        # Texte des catégories
        for text in self.widget.cat_text_items:
            if text is not None:
                if scale < ZOOM_FAR:
                    text.setOpacity(0)
                elif scale > ZOOM_MEDIUM:
                    text.setOpacity(1)
                else:
                    t = (scale - ZOOM_FAR) / (ZOOM_MEDIUM - ZOOM_FAR)
                    text.setOpacity(clamp(t, 0, 1))

        # Notes
        for item in self.widget.note_items:
            if item is not None:
                if scale < ZOOM_FAR:
                    item.setOpacity(0)
                elif scale > ZOOM_MEDIUM:
                    item.setOpacity(1)
                else:
                    t = (scale - ZOOM_FAR) / (ZOOM_MEDIUM - ZOOM_FAR)
                    item.setOpacity(clamp(t, 0, 1))

        # Liens notes → catégories
        for line in self.widget.link_items:
            if line is not None:
                if scale < ZOOM_FAR:
                    line.setOpacity(0)
                elif scale > ZOOM_CLOSE:
                    line.setOpacity(1)
                    line.setPen(QPen(QColor("#bbb"), 1))
                else:
                    t = clamp((scale - ZOOM_FAR) / (ZOOM_CLOSE - ZOOM_FAR), 0, 1)
                    color = QColor.fromRgbF(0.2 + 0.6 * t, 0.2 + 0.6 * t, 0.2 + 0.6 * t)
                    width = interpolate(2.0, 1.0, t)
                    pen = QPen(color, width)
                    line.setPen(pen)
                    line.setOpacity(t)

        # Liens entre catégories
        for line in self.widget.cat_link_items:
            if line is not None:
                if scale < ZOOM_FAR:
                    line.setOpacity(1)
                    line.setPen(QPen(QColor("black"), 2))
                elif scale > ZOOM_CLOSE:
                    # Zoom très proche : très épais et faible opacité
                    line.setOpacity(0.1)
                    line.setPen(QPen(QColor("black"), 4.0))
                else:
                    t = clamp((scale - ZOOM_FAR) / (ZOOM_CLOSE - ZOOM_FAR), 0, 1)
                    width = interpolate(2.0, 4.0, t)
                    opacity = interpolate(1.0, 0.1, t)
                    pen = QPen(QColor("black"), width)
                    line.setPen(pen)
                    line.setOpacity(opacity)



