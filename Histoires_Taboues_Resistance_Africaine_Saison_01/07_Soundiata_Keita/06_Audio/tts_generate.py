#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tts_generate.py — Génère l'audio de narration à partir de Narration_TTS.txt
en utilisant Google Cloud Text-to-Speech, puis assemble le tout avec ffmpeg.

PRÉREQUIS
  1. API "Cloud Text-to-Speech" ACTIVÉE sur le projet Google Cloud + facturation active.
  2. ffmpeg installé et accessible dans le PATH.
  3. Python 3.8+ (utilise seulement la bibliothèque standard : urllib).
  4. Un identifiant d'authentification placé dans une variable d'environnement (voir ci-dessous).
     NE PAS écrire la clé en dur dans ce fichier.

AUTHENTIFICATION (choisir UN mode)
  - Mode "bearer" (jeton OAuth, ex. commençant par "AQ." ou "ya29.", valable ~1h) :
        Windows  PowerShell :  $env:GOOGLE_TTS_TOKEN = "VOTRE_JETON"
        macOS/Linux         :  export GOOGLE_TTS_TOKEN="VOTRE_JETON"
        (obtenir un jeton frais :  gcloud auth print-access-token )
  - Mode "key" (clé API "AIza...") :
        export GOOGLE_TTS_API_KEY="AIza..."
  Le script détecte automatiquement la variable présente.

UTILISATION
    python tts_generate.py
    python tts_generate.py --voice fr-FR-Neural2-D --rate 0.96
    python tts_generate.py --list-voices         # liste les voix françaises et quitte
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

# --------------------------------------------------------------------------- #
TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
VOICES_URL = "https://texttospeech.googleapis.com/v1/voices"
HERE = Path(__file__).resolve().parent
INPUT_TXT = HERE / "Narration_TTS.txt"
OUT_DIR = HERE / "tts_out"
FINAL = HERE / "narration_soundiata.mp3"
MAX_BYTES = 4800           # marge sous la limite de 5000 octets/requête
GAP_SECONDS = 0.8          # silence inséré entre chapitres
# --------------------------------------------------------------------------- #


def auth_headers():
    token = os.environ.get("GOOGLE_TTS_TOKEN")
    key = os.environ.get("GOOGLE_TTS_API_KEY")
    if token:
        return {"Authorization": f"Bearer {token}"}, ""
    if key:
        return {}, f"?key={key}"
    sys.exit("ERREUR : définissez GOOGLE_TTS_TOKEN (jeton OAuth) ou GOOGLE_TTS_API_KEY (clé AIza...).")


def http_post(url, payload):
    headers, suffix = auth_headers()
    headers["Content-Type"] = "application/json; charset=utf-8"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url + suffix, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"ERREUR HTTP {e.code} : {e.read().decode('utf-8', 'ignore')}")


def list_voices():
    headers, suffix = auth_headers()
    req = urllib.request.Request(VOICES_URL + suffix, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode("utf-8"))
    print("Voix françaises disponibles (fr-FR / fr-CA) :\n")
    for v in data.get("voices", []):
        if any(lc.startswith("fr-") for lc in v.get("languageCodes", [])):
            print(f"  {v['name']:<28} {v['ssmlGender']:<8} {','.join(v['languageCodes'])}")


# --------------------------------------------------------------------------- #
#  Découpage du texte
# --------------------------------------------------------------------------- #

def load_chapters(path: Path):
    """Retourne [(titre, texte), ...] en découpant sur les marqueurs [CHAPITRE ...]."""
    raw = path.read_text(encoding="utf-8")
    # On ignore l'en-tête (avant le premier [CHAPITRE) et le [FIN ...].
    parts = re.split(r"\[CHAPITRE[^\]]*\]", raw)
    titles = re.findall(r"\[CHAPITRE[^\]]*\]", raw)
    chapters = []
    for title, body in zip(titles, parts[1:]):
        body = re.split(r"\[FIN[^\]]*\]", body)[0]
        body = body.strip()
        if body:
            num = re.search(r"\d+", title)
            chapters.append((num.group() if num else str(len(chapters) + 1), body))
    if not chapters:  # pas de marqueurs : on prend tout
        chapters = [("01", raw.strip())]
    return chapters


def chunk_text(text: str, max_bytes: int = MAX_BYTES):
    """Découpe un texte en morceaux <= max_bytes, en respectant les phrases."""
    sentences = re.split(r"(?<=[.!?…])\s+", text.replace("\n", " "))
    chunks, cur = [], ""
    for s in sentences:
        candidate = (cur + " " + s).strip()
        if len(candidate.encode("utf-8")) > max_bytes and cur:
            chunks.append(cur.strip())
            cur = s
        else:
            cur = candidate
    if cur.strip():
        chunks.append(cur.strip())
    return chunks


# --------------------------------------------------------------------------- #
#  Synthèse
# --------------------------------------------------------------------------- #

def synthesize(text, voice, lang, rate, pitch):
    payload = {
        "input": {"text": text},
        "voice": {"languageCode": lang, "name": voice},
        "audioConfig": {"audioEncoding": "MP3", "speakingRate": rate, "pitch": pitch},
    }
    resp = http_post(TTS_URL, payload)
    return base64.b64decode(resp["audioContent"])


def make_silence(path: Path, seconds: float):
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i",
         "anullsrc=channel_layout=mono:sample_rate=24000",
         "-t", str(seconds), "-q:a", "9", str(path)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="fr-FR-Neural2-D",
                    help="Voix Google (ex. fr-FR-Neural2-D, fr-FR-Chirp3-HD-Charon)")
    ap.add_argument("--lang", default="fr-FR")
    ap.add_argument("--rate", type=float, default=0.97, help="Vitesse (0.25–4.0)")
    ap.add_argument("--pitch", type=float, default=-1.0, help="Hauteur (-20.0 à 20.0)")
    ap.add_argument("--list-voices", action="store_true")
    args = ap.parse_args()

    if args.list_voices:
        list_voices()
        return

    if not INPUT_TXT.exists():
        sys.exit(f"Introuvable : {INPUT_TXT}")

    OUT_DIR.mkdir(exist_ok=True)
    silence = OUT_DIR / "_silence.mp3"
    make_silence(silence, GAP_SECONDS)

    chapters = load_chapters(INPUT_TXT)
    concat_list = OUT_DIR / "concat.txt"
    entries = []

    for cnum, ctext in chapters:
        chunks = chunk_text(ctext)
        print(f"[Chapitre {cnum}] {len(chunks)} segment(s)…")
        chap_path = OUT_DIR / f"chapitre_{cnum.zfill(2)}.mp3"
        with chap_path.open("wb") as out:
            for i, ch in enumerate(chunks, 1):
                audio = synthesize(ch, args.voice, args.lang, args.rate, args.pitch)
                out.write(audio)
                print(f"   ✓ segment {i}/{len(chunks)} ({len(ch)} car.)")
        entries.append(chap_path)
        entries.append(silence)  # pause entre chapitres

    # Fichier de concaténation ffmpeg
    with concat_list.open("w", encoding="utf-8") as f:
        for p in entries[:-1]:  # pas de silence final
            f.write(f"file '{p.as_posix()}'\n")

    print("Assemblage ffmpeg…")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
         "-c:a", "libmp3lame", "-q:a", "2", str(FINAL)],
        check=True,
    )
    print(f"\n✅ Audio final : {FINAL}")


if __name__ == "__main__":
    main()
