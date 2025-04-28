# app/utils/keyword_extractor.py

import json
from pathlib import Path
import threading

# Pas de spacy importé au début
nlp = None
nlp_ready = False
nlp_lock = threading.Lock()

TERMS_PATH = Path("data/termes_interdits.json")
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
    """Extraction de mots-clés en attendant que le modèle soit prêt."""
    ensure_nlp_ready()

    global nlp

    if not nlp_ready:
        print("⏳ Modèle spaCy pas encore prêt, petite attente...")
        import time
        timeout = 5  # secondes
        start = time.time()
        while not nlp_ready and (time.time() - start) < timeout:
            time.sleep(0.1)

        if not nlp_ready:
            print("❗ Modèle non chargé après 5s, extraction annulée.")
            return []

    doc = nlp(text.lower())
    mots_cles = []
    for token in doc:
        mot = token.lemma_
        if (
            not token.is_stop
            and not token.is_punct
            and not token.like_num
            and len(mot) > 2
            and mot not in termes_interdits
        ):
            mots_cles.append(mot)

    return list(set(mots_cles))[:6]
