# Workflow de Production — Histoires Taboues

> Pipeline standard, de l'idée à la publication. Chaque épisode suit ces 8 étapes.

## Vue d'ensemble

```
01_Recherche → 02_Script → 03_Prompts_Images → 04_Miniature
            → 05_Metadata → 06_Audio → 07_Montage → 08_Publication
```

## Étapes détaillées

### 1. Recherche (`01_Recherche`)
- Rassembler sources primaires, universitaires, chronologie, personnages, bibliographie.
- Critère de sortie : chronologie validée + ≥ 8 sources solides.

### 2. Script (`02_Script`)
- V1 (jet narratif) → V2 (corrigé, sourcé) → Final (prêt voix).
- Respecter la structure imposée en 8 actes. Cible : 5500–6500 mots.
- Critère de sortie : Script_Final relu, sans affirmation non sourcée.

### 3. Prompts images (`03_Prompts_Images`)
- Remplir `prompts_images.csv` : 30 images (10 portraits, 10 scènes, 5 cartes, 5 émotionnelles).
- Critère de sortie : chaque scène du script a au moins une image associée.

### 4. Miniature (`04_Miniature`)
- Rédiger `thumbnail_brief.md`, produire 2–3 variantes, choisir par test A/B.

### 5. Metadata (`05_Metadata`)
- Titre, description, tags, chapitres optimisés SEO (voir Regles_SEO.md).

### 6. Audio (`06_Audio`)
- Narration enregistrée/synthétisée, brief musique, effets sonores.

### 7. Montage (`07_Montage`)
- Storyboard + timeline ; assemblage image/son/texte.

### 8. Publication (`08_Publication`)
- Dérouler `Publication_Checklist.md`. Rien ne sort sans checklist complète.

## Rôles (à adapter)

| Rôle | Responsable | Étapes |
|------|-------------|--------|
| Recherche | _à définir_ | 1 |
| Écriture | _à définir_ | 2 |
| Direction artistique | _à définir_ | 3–4 |
| SEO | _à définir_ | 5 |
| Voix / audio | _à définir_ | 6 |
| Montage | _à définir_ | 7 |
| Publication | _à définir_ | 8 |

<!-- COMMENTAIRE : durée cible par épisode = 25–30 min. Voir Roadmap_Saison_01.md pour le calendrier. -->
