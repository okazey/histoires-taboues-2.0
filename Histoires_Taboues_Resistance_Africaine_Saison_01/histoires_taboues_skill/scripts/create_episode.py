import csv
import re
import sys
from pathlib import Path


def slugify(text: str) -> str:
    text = text.strip().replace("'", " ").replace("’", " ")
    text = re.sub(r"[^A-Za-zÀ-ÿ0-9]+", "_", text)
    return text.strip("_")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def create_prompts_csv(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = ["Scene_ID", "Chapitre", "Type", "Description", "Prompt_Flow", "Prompt_Whisk", "Prompt_Midjourney", "Statut"]
    rows = []
    types = ["Portrait"] * 10 + ["Scene historique"] * 10 + ["Carte"] * 5 + ["Emotion"] * 5
    for i, t in enumerate(types, start=1):
        rows.append([f"S{i:02d}", "À compléter", t, "À compléter", "À compléter", "À compléter", "À compléter", "À générer"])
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def main():
    if len(sys.argv) < 3:
        print('Usage: python scripts/create_episode.py "Sujet" "Titre provisoire"')
        sys.exit(1)

    subject = sys.argv[1]
    title = sys.argv[2]
    folder = Path(f"Episode_{slugify(subject)}")
    folder.mkdir(exist_ok=True)

    write(folder / "README.md", f"""
# {subject}

Titre provisoire : {title}

Objectif : produire un épisode documentaire YouTube prêt à uploader pour la chaîne Histoires Taboues.

Durée cible : 25 à 35 minutes.
Script cible : 5500 à 6500 mots.
""")

    write(folder / "01_Recherche/Sources_Primaires.md", f"""
# Sources primaires — {subject}

## Archives
- À vérifier

## Documents historiques
- À vérifier

## Citations utilisables
Attention : ne jamais inventer une citation.

## Ce qui est certain
- À compléter

## Ce qui est probable
- À compléter

## Ce qui est débattu
- À compléter

## Ce qu'il ne faut pas affirmer
- À compléter
""")

    write(folder / "01_Recherche/Sources_Universitaires.md", """
# Sources universitaires

Objectif : minimum 5 sources sérieuses.

| Source | Auteur | Année | Type | Idées utiles | Fiabilité |
|---|---|---:|---|---|---|
| À compléter |  |  |  |  |  |
""")

    write(folder / "01_Recherche/Chronologie.md", """
# Chronologie

| Date | Événement | Source | Niveau de certitude |
|---|---|---|---|
| À compléter | À compléter | À compléter | À vérifier |
""")

    write(folder / "01_Recherche/Personnages.md", """
# Personnages

| Nom | Rôle | Camp | Fonction narrative | Notes |
|---|---|---|---|---|
| À compléter | À compléter | À compléter | À compléter | À compléter |
""")

    write(folder / "01_Recherche/Notes_Fact_Checking.md", """
# Notes de vérification historique

## Dates sensibles
- À vérifier

## Citations sensibles
- À vérifier

## Épisodes controversés
- À vérifier

## Risques d'anachronisme
- À vérifier
""")

    script_template = f"""
# Script — {subject}

Titre provisoire : {title}

## 0:00 — Hook choc
À écrire. Objectif : capturer l'attention en moins de 20 secondes.

## Contexte historique
À écrire.

## Ascension
À écrire.

## Pourquoi il/elle dérangeait
À écrire.

## Affrontement avec l'empire
À écrire.

## Trahisons ou basculement
À écrire.

## Chute
À écrire.

## Pourquoi on l'a oublié
À écrire.

## Héritage
À écrire.

## Teaser vidéo suivante
À écrire.

## Appel à l'abonnement
À placer vers 6 à 8 minutes :
Si vous aimez découvrir les histoires que les manuels oublient, abonnez-vous maintenant.
"""
    write(folder / "02_Script/Script_V1.md", script_template)
    write(folder / "02_Script/Script_Retention.md", script_template.replace("Script", "Script optimisé rétention"))
    write(folder / "02_Script/Script_Final.md", script_template.replace("Script", "Script final"))

    create_prompts_csv(folder / "03_Prompts_Images/prompts_images.csv")

    write(folder / "04_Miniature/thumbnail_brief.md", f"""
# Brief miniature — {subject}

## Objectif
CTR cible : 8 % ou plus.

## Formule
Visage puissant + émotion + texte court + contraste fort.

## Texte miniature
Maximum 4 mots.

Propositions :
1. À compléter
2. À compléter
3. À compléter

## Composition
- Visage dominant à gauche ou centre
- Élément colonial ou militaire en arrière-plan
- Contraste noir/blanc ou sépia dramatique
- Lisible sur smartphone

## À éviter
- Trop de texte
- Détails illisibles
- Images trop chargées
- Anachronismes
""")

    write(folder / "04_Miniature/prompt_miniature.md", """
# Prompt miniature

À générer après validation du script final.

Style recommandé : miniature YouTube documentaire historique, contraste fort, émotion claire, ultra-réaliste, noir et blanc ou sépia léger, 16:9, texte court lisible.
""")

    write(folder / "05_Metadata/Titre.md", f"""
# Titres YouTube — {subject}

## Titre final
{title}

## Alternatives
1. À compléter
2. À compléter
3. À compléter
4. À compléter
5. À compléter
""")

    write(folder / "05_Metadata/Description.md", """
# Description YouTube

À écrire.

Inclure le mot-clé principal dans les deux premières lignes.

## Hashtags
#HistoiresTaboues #Afrique #HistoireAfricaine #Colonisation #ResistanceAfricaine
""")

    write(folder / "05_Metadata/Tags.md", """
# Tags YouTube

À compléter : 15 à 25 tags.
""")

    write(folder / "05_Metadata/Chapitres.md", """
# Chapitres YouTube

00:00 - Hook
01:00 - Contexte historique
05:00 - Ascension
10:00 - Le conflit
20:00 - La chute
27:00 - Héritage
""")

    write(folder / "05_Metadata/Commentaire_Epingle.md", """
# Commentaire épinglé

À écrire.

Objectif : provoquer une discussion respectueuse.
Exemple :
Selon vous, pourquoi cette histoire reste-t-elle si peu enseignée aujourd'hui ?
""")

    write(folder / "06_Audio/Narration_TTS.md", """
# Narration TTS

Coller ici le script final nettoyé pour ElevenLabs ou autre outil TTS.

Règles :
- phrases courtes
- ponctuation claire
- respirations naturelles
- pas de notes de montage
""")

    write(folder / "06_Audio/Prompt_Musique.md", """
# Prompt musique

Musique instrumentale documentaire historique, sombre, émotionnelle, tension progressive, percussions graves, flûte ou kora discrète, ambiance africaine respectueuse, pas de chant, pas de paroles, montée dramatique lente, 30 minutes, cinematic documentary score.
""")

    write(folder / "06_Audio/Effets_Sonores.md", """
# Effets sonores

| Timecode | Ambiance | Effet sonore | Intensité |
|---|---|---|---|
| 00:00 | Tension | Vent grave | Faible |
| À compléter | À compléter | À compléter | À compléter |
""")

    write(folder / "07_Montage/Storyboard.md", """
# Storyboard

| Timecode | Narration résumée | Image | Mouvement caméra | Son |
|---|---|---|---|---|
| 00:00 | Hook | Portrait dramatique | Zoom lent | Drone grave |
| À compléter | À compléter | À compléter | À compléter | À compléter |
""")

    write(folder / "07_Montage/Timeline.md", """
# Timeline de montage

00:00 Hook
01:00 Contexte
05:00 Ascension
10:00 Guerre
20:00 Chute
27:00 Héritage
""")

    write(folder / "08_Publication/Checklist_Publication.md", """
# Checklist publication

- [ ] Script final validé
- [ ] Sources vérifiées
- [ ] Images générées
- [ ] Narration exportée
- [ ] Musique exportée
- [ ] Montage terminé
- [ ] Miniature validée
- [ ] Titre validé
- [ ] Description validée
- [ ] Tags validés
- [ ] Chapitres ajoutés
- [ ] Commentaire épinglé préparé
- [ ] Sous-titres vérifiés
- [ ] Upload programmé mardi ou samedi à 23h30
""")

    print(f"Épisode créé : {folder}")


if __name__ == "__main__":
    main()
