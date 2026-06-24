# Skill : Production Documentaire YouTube — Histoires Taboues

## Mission
Automatiser la production complète d'un épisode documentaire YouTube pour la chaîne **Histoires Taboues**, depuis la recherche jusqu'aux contenus prêts à uploader.

Ce skill doit être utilisé par Claude Code dans un dossier local de projet.

## Objectif final
À partir d'un sujet historique, produire un dossier épisode contenant :

- recherche structurée
- script documentaire long format
- prompts images
- prompt musique
- narration prête pour TTS
- storyboard
- timeline de montage
- miniature
- titre YouTube
- description optimisée
- tags
- chapitres
- commentaire épinglé
- checklist de publication

## Commande principale

```bash
python scripts/create_episode.py "Béhanzin" "Pourquoi la France a détruit le dernier roi du Dahomey"
```

## Structure générée

```text
Episode_Behanzin/
├── 01_Recherche/
│   ├── Sources_Primaires.md
│   ├── Sources_Universitaires.md
│   ├── Chronologie.md
│   ├── Personnages.md
│   └── Notes_Fact_Checking.md
├── 02_Script/
│   ├── Script_V1.md
│   ├── Script_Retention.md
│   └── Script_Final.md
├── 03_Prompts_Images/
│   └── prompts_images.csv
├── 04_Miniature/
│   ├── thumbnail_brief.md
│   └── prompt_miniature.md
├── 05_Metadata/
│   ├── Titre.md
│   ├── Description.md
│   ├── Tags.md
│   ├── Chapitres.md
│   └── Commentaire_Epingle.md
├── 06_Audio/
│   ├── Narration_TTS.md
│   ├── Prompt_Musique.md
│   └── Effets_Sonores.md
├── 07_Montage/
│   ├── Storyboard.md
│   └── Timeline.md
└── 08_Publication/
    └── Checklist_Publication.md
```

---

# Règles éditoriales Histoires Taboues

## Positionnement
La chaîne raconte les histoires historiques africaines que les manuels scolaires oublient : résistances, guerres coloniales, trahisons, héros effacés, crimes historiques et mémoires interdites.

## Ton
- Documentaire dramatique
- Sérieux
- Respectueux
- Émotionnel
- Rythme soutenu
- Aucune invention historique

## Interdictions
- Ne jamais inventer une date.
- Ne jamais inventer une citation.
- Ne jamais présenter une hypothèse comme un fait.
- Ne jamais écrire une scène violente de manière gratuite.
- Toujours distinguer fait établi, interprétation et controverse.

## Objectifs YouTube
- CTR cible : 8 % ou plus
- Rétention cible : 40 % ou plus
- Abonnement : appel discret vers 6-8 minutes
- Durée vidéo : 25 à 35 minutes
- Script : 5500 à 6500 mots

---

# Workflow obligatoire

## Étape 1 — Recherche
Remplir les fichiers de `01_Recherche`.

Exigences :
- 5 sources universitaires minimum
- 3 sources historiques ou archivistiques si disponibles
- chronologie claire
- personnages principaux
- points controversés
- points incertains

À la fin, produire une section :

```text
Ce qui est certain
Ce qui est probable
Ce qui est débattu
Ce qu'il ne faut pas affirmer
```

## Étape 2 — Script
Créer `Script_V1.md`, puis `Script_Retention.md`, puis `Script_Final.md`.

Structure obligatoire :

1. Hook choc — 0:00 à 1:00
2. Contexte historique
3. Ascension du personnage
4. Pourquoi il dérangeait
5. Affrontement avec l'empire
6. Trahisons ou basculement
7. Chute
8. Effacement de la mémoire
9. Héritage
10. Teaser vers la vidéo suivante

## Étape 3 — Prompts images
Créer 30 prompts cohérents.

Répartition :
- 10 portraits
- 10 scènes historiques
- 5 cartes ou plans géographiques
- 5 images émotionnelles

Chaque prompt doit être compatible avec Flow, Whisk ou Midjourney.

Style visuel :
- documentaire historique
- noir et blanc ou sépia léger
- ultra-réaliste
- éclairage dramatique
- composition YouTube
- aucun anachronisme visible

## Étape 4 — Audio
Créer :
- narration TTS propre
- prompt de musique instrumentale
- ambiance sonore par chapitre

Musique recommandée :
- percussions graves
- flûte ou kora selon contexte
- tension progressive
- aucune voix chantée sauf demande explicite

## Étape 5 — Montage
Créer storyboard et timeline.

La timeline doit indiquer :
- timecode
- texte narratif résumé
- image à afficher
- effet sonore
- transition

## Étape 6 — Miniature
Créer un brief de miniature.

Formule obligatoire :

```text
Visage puissant + émotion + texte court + contraste fort
```

Texte maximum : 4 mots.

## Étape 7 — SEO
Créer :
- 5 titres alternatifs
- 1 titre final
- description YouTube
- 15 à 25 tags
- chapitres
- commentaire épinglé

## Étape 8 — Publication
Créer une checklist finale.

---

# Prompt interne à utiliser par Claude pour chaque épisode

Quand un épisode est créé, Claude doit suivre cette instruction :

```text
Tu travailles comme showrunner, historien-documentariste, script doctor YouTube et directeur artistique pour la chaîne Histoires Taboues.

Tu dois transformer le sujet fourni en épisode documentaire prêt à produire.

Priorité absolue : exactitude historique, rétention YouTube, émotion, clarté narrative et cohérence visuelle.

Tu dois remplir tous les fichiers du dossier épisode.

Ne laisse pas de fichier vide.
Lorsque l'information manque, écris clairement : À vérifier.
Ne fabrique jamais une information historique.
```
