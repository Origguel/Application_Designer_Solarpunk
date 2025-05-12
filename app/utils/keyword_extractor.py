import json
from pathlib import Path
import spacy

# ✅ Chargement immédiat de spaCy au lancement
nlp = spacy.load("fr_core_news_sm")
print("✅ Modèle spaCy chargé (au lancement).")

TERMS_PATH = Path("assets/keyword/termes_interdits.json")
if TERMS_PATH.exists():
    with TERMS_PATH.open(encoding="utf-8") as f:
        termes_interdits = set(json.load(f))
else:
    termes_interdits = set()


def extract_keywords(text):
    doc = nlp(text.lower())
    candidates = {}

    for token in doc:
        mot = token.lemma_.lower()
        if token.pos_ == "PROPN" or len(mot) <= 4:
            mot = token.text.lower()
            print(f"🧪 Lemme modifié : {token.text} → {mot}")
        pos = token.pos_

        # ❌ Filtres de base
        if token.is_stop or token.is_punct or token.like_num:
            continue
        if len(mot) < 3 or mot in termes_interdits:
            continue
        if not mot.isalpha():
            continue
        if sum(1 for c in mot if c in "aeiouy") < 2:
            continue

        # ✅ POS ciblés
        if pos in {"NOUN", "PROPN", "ADJ"}:
            score = 1
            if pos == "PROPN":
                score += 2
            elif pos == "ADJ":
                score += 0.5
            if mot in candidates:
                candidates[mot] += score
            else:
                candidates[mot] = score

    # 🔽 Tri par pertinence, puis unicité
    sorted_keywords = sorted(candidates.items(), key=lambda x: -x[1])
    mots_uniques = []
    seen = set()
    for mot, _ in sorted_keywords:
        if mot not in seen:
            seen.add(mot)
            mots_uniques.append(mot)

    return mots_uniques[:6]
