# app/components/note/note_creator.py
from __future__ import annotations

import json
import shutil
from pathlib import Path
from datetime import datetime

# Dépendances existantes dans ton projet
from app.utils.keyword_extractor import extract_keywords
from app.utils.categorie_manager.category_manager import CategoryManager
from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater

# ======================================================================
#                         CONFIG & CONSTANTES
# ======================================================================

NOTES_DIR = Path("data/notes")
CONTENU_BASE_DIR = NOTES_DIR / "contenu"
DIR_TEXTE = CONTENU_BASE_DIR / "texte"
DIR_IMAGE = CONTENU_BASE_DIR / "image"
DIR_LIEN  = CONTENU_BASE_DIR / "lien"

for _d in (NOTES_DIR, DIR_TEXTE, DIR_IMAGE, DIR_LIEN):
    _d.mkdir(parents=True, exist_ok=True)

# "B" = aaaa -> baaa (ton exemple) ; "A" = aaaa -> aaab (classique)
ALPHA_ID_ORDER = "B"

# ======================================================================
#                        OUTILS : ID alphanumérique
# ======================================================================

def _to_num(s: str, order: str = "A") -> int:
    base = 26
    s = s.lower()
    if order == "A":
        acc = 0
        for c in s:
            acc = acc * base + (ord(c) - 97)
        return acc
    else:
        acc, mul = 0, 1
        for c in s:
            acc += (ord(c) - 97) * mul
            mul *= base
        return acc

def _from_num(n: int, order: str = "A") -> str:
    base = 26
    chars = ['a', 'a', 'a', 'a']
    if order == "A":
        for i in range(3, -1, -1):
            chars[i] = chr(97 + (n % base))
            n //= base
    else:
        for i in range(0, 4):
            chars[i] = chr(97 + (n % base))
            n //= base
    return "".join(chars)

def next_alpha_id(order: str = ALPHA_ID_ORDER) -> str:
    import re
    pattern = re.compile(r"([a-z]{4})\.json$", re.I)
    max_n = -1
    for f in NOTES_DIR.glob("*.json"):
        m = pattern.match(f.name)
        if m:
            n = _to_num(m.group(1), order)
            if n > max_n:
                max_n = n
    return _from_num(max_n + 1 if max_n >= 0 else 0, order)

# ======================================================================
#                        OUTILS : écriture contenus
# ======================================================================

def _write_text(note_id: str, texte: str) -> dict:
    p = DIR_TEXTE / f"{note_id}_texte.json"
    with p.open("w", encoding="utf-8") as f:
        json.dump({"id": note_id, "type": "texte", "texte": texte},
                  f, ensure_ascii=False, indent=4)
    return {"type": "texte", "contenu": str(p.relative_to(NOTES_DIR).as_posix())}

def _write_link(note_id: str, url: str) -> dict:
    p = DIR_LIEN / f"{note_id}_lien.json"
    with p.open("w", encoding="utf-8") as f:
        json.dump({"id": note_id, "type": "lien", "lien": url},
                  f, ensure_ascii=False, indent=4)
    return {"type": "lien", "contenu": str(p.relative_to(NOTES_DIR).as_posix())}

def _write_image(note_id: str, src_image_path: str) -> dict:
    src = Path(src_image_path)
    ext = src.suffix.lower() or ".png"
    dest = DIR_IMAGE / f"{note_id}_image{ext}"
    shutil.copy2(src, dest)
    return {"type": "image", "contenu": str(dest.relative_to(NOTES_DIR).as_posix())}

# ======================================================================
#                      OUTILS : normalisation & groupage
# ======================================================================

def _normalize_type(t: str) -> str:
    if not t:
        return ""
    t = t.strip().lower()
    mapping = {
        "text": "texte", "texte": "texte", "string": "texte",
        "link": "lien", "lien": "lien", "url": "lien",
        "image": "image", "img": "image", "picture": "image", "photo": "image",
        "multi": "multi",
        # non encore gérés à l'écriture :
        "video": "video", "doc": "doc", "code": "code",
    }
    return mapping.get(t, t)

def _group_ordered(items: list[dict]) -> list[dict]:
    groups = {"texte": [], "image": [], "lien": []}
    for it in items:
        typ = it.get("type")
        if typ in groups:
            groups[typ].append(it)
    ordered = []
    if groups["texte"]:
        ordered.append({"1_texte": groups["texte"]})
    if groups["image"]:
        ordered.append({"2_image": groups["image"]})
    if groups["lien"]:
        ordered.append({"3_lien": groups["lien"]})
    return ordered

# ======================================================================
#                               CREATOR
# ======================================================================

class NoteCreator:
    @staticmethod
    def create_note(
        title: str,
        date_str: str,
        note_type: str,
        project: str,
        description: str,
        contenu
    ) -> dict:
        """
        Nouveau format strict (plus de champs legacy):
        - legacy accepté à l'appel (texte/lien/image + contenu=str),
        - ou multi: contenu=list[{"type":..., "value":...}]
        """
        # 1) ID
        note_id = next_alpha_id(order=ALPHA_ID_ORDER)

        # 2) Keywords
        keywords = extract_keywords(description)

        # 3) Contenus
        contents: list[dict] = []
        note_type_norm = _normalize_type(note_type)

        if isinstance(contenu, list) and note_type_norm == "multi":
            for item in contenu:
                t = _normalize_type(item.get("type", ""))
                v = item.get("value", "")
                if t == "texte" and v:
                    contents.append(_write_text(note_id, v))
                elif t == "lien" and v:
                    contents.append(_write_link(note_id, v))
                elif t == "image" and v:
                    contents.append(_write_image(note_id, v))
                else:
                    pass
        else:
            if note_type_norm == "texte" and contenu:
                contents.append(_write_text(note_id, str(contenu)))
            elif note_type_norm == "lien" and contenu:
                contents.append(_write_link(note_id, str(contenu)))
            elif note_type_norm == "image" and contenu:
                contents.append(_write_image(note_id, str(contenu)))
            else:
                # fallback texte pour éviter une note vide
                if contenu:
                    contents.append(_write_text(note_id, str(contenu)))

        # 4) Dates
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y") if date_str else datetime.now()
        except Exception:
            dt = datetime.now()

        dates_block = [{
            "format": "DD/MM/YYYY",
            "date_creation": dt.strftime("%d/%m/%Y"),
            "date_derniere_modification": dt.strftime("%d/%m/%Y"),
            "date_derniere_ouverture": dt.strftime("%d/%m/%Y"),
        }]

        # 5) Type pour infos[]
        computed_type = "multi" if len(contents) > 1 else (contents[0]["type"] if contents else "texte")

        # 6) Schéma final (SANS champs legacy)
        note_data = {
            "id": note_id,
            "dates": dates_block,
            "infos": [{
                "title": title,
                "description": description,
                "project": project,
                "type": computed_type
            }],
            "keywords": keywords,
            "note_contenu": _group_ordered(contents)
        }

        # 7) Écriture
        file_path = NOTES_DIR / f"{note_id}.json"
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(note_data, f, ensure_ascii=False, indent=4)

        # 8) MAJ catégories + arbre
        try:
            CategoryManager().update()
        except Exception as e:
            print(f"⚠️ CategoryManager.update() a échoué : {e}")

        try:
            CategoryTreeUpdater().add_note(note_id, keywords)
        except Exception as e:
            print(f"⚠️ CategoryTreeUpdater.add_note() a échoué : {e}")

        return note_data
