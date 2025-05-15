from PySide6.QtCore import QRectF, QPoint
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication


class TimelineNoteHoverHandler:
    def __init__(self, canvas):
        self.canvas = canvas
        self.items = []
        self.hovered_item = None
        self.selected_item = None

    def clear_items(self):
        self.items.clear()
        self.hovered_item = None

    def register_item(self, item):
        self.items.append(item)

    def handle_hover(self, pos: QPoint):
        hovered = None
        for item in self.items:
            if item.contains(pos):
                hovered = item
                print(f"🟠 Hover détecté sur note à x={item.x}")
                break

        if hovered is not self.hovered_item:
            if self.hovered_item:
                print("🔵 Fin de hover précédent")
                self.hovered_item.set_highlight(False)
            self.hovered_item = hovered
            if self.hovered_item:
                print("🟠 Nouveau hover actif")
                self.hovered_item.set_highlight(True)
            self.canvas.update()
            return True
        return False



    def handle_click(self, pos: QPoint):
        for item in self.items:
            if item.contains(pos):
                if self.selected_item:
                    self.selected_item.set_selected(False)
                item.set_selected(True)
                self.selected_item = item
                self.canvas.update()  # ✅ Ajout ici aussi
                return True
        return False

