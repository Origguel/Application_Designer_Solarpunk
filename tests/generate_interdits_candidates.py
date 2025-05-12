# tests/generate_interdits_candidates.py

import json
from pathlib import Path
from collections import Counter
from app.utils.keyword_extractor import extract_keywords

NOTES_DIR = Path("data/notes")
TERMS_PATH = Path("assets/keyword/termes_interdits.json")

def is_suspect(word):
    voyelles = "aeiouy"
    nb_voyelles = sum(1 for c in word if c in voyelles)
    if nb_voyelles < 2:
        return True
    if not word.isalpha():
        return True
    if len(word) < 4:
        return True
    return False

def generate_interdits_candidates():
    counter = Counter()
    for file in NOTES_DIR.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            description = data.get("description", "")
            keywords = extract_keywords(description)
            counter.update(keywords)

    candidats = [kw for kw, freq in counter.items() if is_suspect(kw) and freq >= 2]

    print(f"\n🔎 {len(candidats)} mots-clés suspects trouvés :\n")
    for kw in candidats:
        print(f"- {kw} ({counter[kw]} occurences)")

    # Proposer d'ajouter au fichier
    if not candidats:
        print("✅ Aucun mot suspect à ajouter.")
        return

    choix = input("\nSouhaitez-vous ajouter ces mots à termes_interdits.json ? (y/n) ").lower()
    if choix == "y":
        if TERMS_PATH.exists():
            with TERMS_PATH.open(encoding="utf-8") as f:
                interdits = set(json.load(f))
        else:
            interdits = set()

        interdits.update(candidats)
        with TERMS_PATH.open("w", encoding="utf-8") as f:
            json.dump(sorted(interdits), f, ensure_ascii=False, indent=4)

        print("✅ Mots ajoutés à termes_interdits.json.")

if __name__ == "__main__":
    generate_interdits_candidates()
