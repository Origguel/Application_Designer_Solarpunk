# app/utils/note_content_writer.py
import json, shutil
from pathlib import Path

BASE = Path("data/notes/contenu")
DIRS = {"texte": BASE/"texte", "image": BASE/"image", "lien": BASE/"lien"}
for d in DIRS.values(): d.mkdir(parents=True, exist_ok=True)

def write_text(note_id: str, texte: str):
    p = DIRS["texte"] / f"{note_id}_texte.json"
    json.dump({"id": note_id, "type": "texte", "texte": texte}, p.open("w", encoding="utf-8"), ensure_ascii=False, indent=4)
    return {"type": "texte", "contenu": str(p.relative_to("data/notes"))}

def write_link(note_id: str, url: str):
    p = DIRS["lien"] / f"{note_id}_lien.json"
    json.dump({"id": note_id, "type": "lien", "lien": url}, p.open("w", encoding="utf-8"), ensure_ascii=False, indent=4)
    return {"type": "lien", "contenu": str(p.relative_to("data/notes"))}

def write_image(note_id: str, src_image_path: str):
    dest = DIRS["image"] / f"{note_id}_image{Path(src_image_path).suffix.lower()}"
    shutil.copy2(src_image_path, dest)
    # on référence directement l’image (pas besoin d’un .json à côté)
    return {"type": "image", "contenu": str(dest.relative_to("data/notes"))}
