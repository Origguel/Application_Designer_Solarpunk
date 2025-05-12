# app/utils/keyword_extractor.py

import json
from pathlib import Path
import threading

# Pas de spacy importé au début
nlp = None
nlp_ready = False
nlp_lock = threading.Lock()

TERMS_PATH = Path("assets/keyword/termes_interdits.json")
if TERMS_PATH.exists():
    with TERMS_PATH.open(encoding="utf-8") as f:
        termes_interdits = set(json.load(f))
else:
    termes_interdits = set()

def _load_nlp_model():
    """Charge spaCy dans un thread."""
    global nlp, nlp_ready
    import spacy  # 👈 Import spacy ici seulement
    nlp = spacy.load("fr_core_news_sm")
    with nlp_lock:
        nlp_ready = True
    print("✅ Modèle spaCy chargé.")

def ensure_nlp_ready():
    """Assure que le modèle est chargé (sinon lance le thread)."""
    global nlp_ready

    if not nlp_ready:
        print("⚡ Chargement du modèle spaCy déclenché...")
        threading.Thread(target=_load_nlp_model, daemon=True).start()

def extract_keywords(text):
    ensure_nlp_ready()

    global nlp

    if not nlp_ready:
        print("⏳ Modèle spaCy pas encore prêt, petite attente...")
        import time
        timeout = 5
        start = time.time()
        while not nlp_ready and (time.time() - start) < timeout:
            time.sleep(0.1)

        if not nlp_ready:
            print("❗ Modèle non chargé après 5s, extraction annulée.")
            return []

    doc = nlp(text.lower())
    candidates = {}

    for token in doc:
        mot = token.lemma_.lower()
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
