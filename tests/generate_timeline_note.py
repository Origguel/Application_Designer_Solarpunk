from pathlib import Path
import json
from datetime import datetime

# 📁 Dossier des notes (individuelles)
notes_dir = Path("data/notes")

# 📁 Chemin final du fichier index
index_path = Path("data/timeline/note_index_by_date.json")

# 📁 S'assurer que le dossier "timeline" existe
index_path.parent.mkdir(parents=True, exist_ok=True)

# 📦 Index de notes par date
index = {}

for note_file in notes_dir.glob("*.json"):
    try:
        with open(note_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_date = data.get("date")
        if not raw_date:
            continue

        # 📅 Conversion au format ISO (YYYY-MM-DD)
        dt = datetime.strptime(raw_date, "%d/%m/%Y")
        date_key = dt.strftime("%Y-%m-%d")
        index.setdefault(date_key, []).append(data["id"])

    except Exception as e:
        print(f"❌ Erreur lecture {note_file.name} : {e}")

# 💾 Sauvegarde
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

print(f"✅ Index sauvegardé dans : {index_path}")
