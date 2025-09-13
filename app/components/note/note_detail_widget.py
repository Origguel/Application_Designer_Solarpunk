from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from pathlib import Path
import json

from app.components.buttons.button_icon import ButtonIcon
from app.components.buttons.button_text_small import ButtonTextSmall
from app.components.labels.label_default import LabelDefault
from app.utils.layouts.flow_layout import FlowLayout
from app.components.badges.keywordbadge import KeywordBadge


DATA_NOTES_DIR = Path("data/notes")


def _safe_get_info(note_data: dict) -> dict:
    """Retourne le bloc infos[0] (nouveau format) ou un fallback legacy."""
    if isinstance(note_data.get("infos"), list) and note_data["infos"]:
        return note_data["infos"][0]
    # fallback legacy (au cas où)
    return {
        "title": note_data.get("title", ""),
        "description": note_data.get("description", ""),
        "project": note_data.get("project", ""),
        "type": note_data.get("type", "")
    }


def _safe_get_date(note_data: dict) -> str:
    """Retourne dates[0].date_creation ou fallback legacy."""
    if isinstance(note_data.get("dates"), list) and note_data["dates"]:
        d0 = note_data["dates"][0]
        return d0.get("date_creation", "") or d0.get("date_derniere_modification", "") or d0.get("date_derniere_ouverture", "")
    return note_data.get("date", "")


def _load_json_from_relpath(relpath: str) -> dict:
    """Charge un JSON depuis un chemin relatif à data/notes."""
    try:
        p = DATA_NOTES_DIR / Path(relpath)
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _read_text_content(relpath: str) -> str:
    data = _load_json_from_relpath(relpath)
    return data.get("texte", "") if isinstance(data, dict) else ""


def _read_link_content(relpath: str) -> str:
    data = _load_json_from_relpath(relpath)
    return data.get("lien", "") if isinstance(data, dict) else ""


def _load_pixmap_from_relpath(relpath: str) -> QPixmap:
    p = DATA_NOTES_DIR / Path(relpath)
    pm = QPixmap(str(p))
    return pm


class NoteDetailWidget(QFrame):
    def __init__(self, note_data, x=408, parent=None):
        super().__init__(parent)
        self.setObjectName("NoteDetailWidget")
        self.setFixedWidth(x)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)

        # --------- Lecture des infos au nouveau format ---------
        info = _safe_get_info(note_data)
        title = info.get("title", "")
        description = info.get("description", "")
        project = info.get("project", "")
        date_str = _safe_get_date(note_data)
        keywords = note_data.get("keywords", []) or []

        # --------- Titre + bouton fermeture ----------
        note_name = LabelDefault(style="H1", text=title, x=None)
        self.note_close_button = ButtonIcon(icon_name="arrow_big_right", icon_color="white", style="Button_Orange")

        self.note_detail_top = QWidget(self)
        note_detail_top_layout = QHBoxLayout(self.note_detail_top)
        note_detail_top_layout.setSpacing(12)
        note_detail_top_layout.setContentsMargins(0, 0, 0, 0)
        note_detail_top_layout.addWidget(note_name, alignment=Qt.AlignTop | Qt.AlignLeft)
        note_detail_top_layout.addWidget(self.note_close_button, alignment=Qt.AlignTop | Qt.AlignRight)
        self.note_detail_top.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # --------- Contenus (nouveau format) ----------
        self.contents_widget = QWidget(self)
        contents_layout = QVBoxLayout(self.contents_widget)
        contents_layout.setSpacing(8)
        contents_layout.setContentsMargins(0, 0, 0, 0)

        note_contenu = note_data.get("note_contenu", [])
        if isinstance(note_contenu, list) and note_contenu:
            # Chaque élément est un dict avec "1_texte" / "2_image" / "3_lien"
            for group in note_contenu:
                # 1) textes
                if "1_texte" in group:
                    for item in group["1_texte"]:
                        rel = item.get("contenu", "")
                        txt = _read_text_content(rel)
                        if txt:
                            lbl = LabelDefault(style="Text", text=txt, x=None)
                            lbl.setWordWrap(True)
                            contents_layout.addWidget(lbl)
                # 2) images
                if "2_image" in group:
                    for item in group["2_image"]:
                        rel = item.get("contenu", "")
                        pm = _load_pixmap_from_relpath(rel)
                        if not pm.isNull():
                            img = QLabel()
                            img.setPixmap(pm)
                            img.setScaledContents(True)
                            img.setMaximumWidth(self.width() - 32)  # marge visuelle
                            contents_layout.addWidget(img)
                # 3) liens
                if "3_lien" in group:
                    for item in group["3_lien"]:
                        rel = item.get("contenu", "")
                        url = _read_link_content(rel)
                        if url:
                            link_lbl = LabelDefault(style="Text", text=url, x=None)
                            link_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
                            contents_layout.addWidget(link_lbl)
        else:
            # ------- Fallback legacy si jamais une vieille note passe encore -------
            contenu_clean = note_data.get("contenu", "").strip()
            if contenu_clean:
                lbl = LabelDefault(style="Text", text=contenu_clean, x=None)
                contents_layout.addWidget(lbl)

        # --------- Projet + date (sur une seule ligne) ----------
        note_projet_label = LabelDefault(style="Text", text=project)
        note_projet_label.setWordWrap(False)
        note_projet_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        note_date_label = LabelDefault(style="Text", text=date_str)

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFixedHeight(6)
        separator_line.setFixedWidth(1)
        separator_line.setStyleSheet("background-color: white; border: none;")

        project_date_widget = QWidget()
        project_date_layout = QHBoxLayout(project_date_widget)
        project_date_layout.setContentsMargins(0, 0, 0, 0)
        project_date_layout.setSpacing(6)
        project_date_layout.addWidget(note_projet_label)
        project_date_layout.addWidget(separator_line)
        project_date_layout.addWidget(note_date_label)
        project_date_layout.addStretch()

        # --------- Mots-clés ----------
        note_keywords_widget = QWidget()
        note_keywords_layout = FlowLayout(note_keywords_widget, spacing=6)
        for keyword in keywords:
            badge = KeywordBadge(text=keyword)
            badge.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            note_keywords_layout.addWidget(badge)

        # --------- Description ----------
        note_description = LabelDefault(style="Text", text=description)

        # --------- "plus de détails" ----------
        note_more_button = ButtonTextSmall(text="plus de détails")
        note_more_button.setStyleSheet("color: #FCF7F3;")
        self.note_more_detail = QWidget(self)
        note_more_detail_layout = QVBoxLayout(self.note_more_detail)
        note_more_detail_layout.setSpacing(6)
        note_more_detail_layout.setContentsMargins(0, 0, 0, 0)
        note_more_detail_layout.addWidget(project_date_widget)
        note_more_detail_layout.addWidget(note_keywords_widget)
        note_more_detail_layout.addWidget(note_description)

        self.note_detail_bottom = QWidget(self)
        note_detail_bottom_layout = QVBoxLayout(self.note_detail_bottom)
        note_detail_bottom_layout.setSpacing(6)
        note_detail_bottom_layout.setContentsMargins(0, 0, 0, 0)
        note_detail_bottom_layout.addWidget(note_more_button)
        note_detail_bottom_layout.addWidget(self.note_more_detail)

        # --------- Layout principal ----------
        note_detail_layout = QVBoxLayout(self)
        note_detail_layout.setSpacing(24)
        note_detail_layout.setContentsMargins(16, 16, 16, 16)
        note_detail_layout.addWidget(self.note_detail_top)
        note_detail_layout.addWidget(self.contents_widget)   # ← remplace l'ancien Label "contenu"
        note_detail_layout.addWidget(self.note_detail_bottom)

        # --------- Interaction ----------
        self.note_close_button.clicked.connect(self.close_parent_detail)

        self.adjustSize()

    def close_parent_detail(self):
        if self.parent():
            self.parent().close_note_detail()
