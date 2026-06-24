# Histoires_Taboues_Resistance_Africaine_Saison_01

Système de production documentaire pour la chaîne YouTube **Histoires Taboues**.
Saison 01 — **Résistance Africaine**.

## Mission
> « Raconter les histoires africaines que les manuels scolaires oublient. »

## Arborescence
```
Histoires_Taboues_Resistance_Africaine_Saison_01/
├── 00_Guidelines/     Ligne éditoriale, style, workflow, miniatures, SEO, checklist
├── 01_Behanzin/       … 07_Soundiata_Keita/  (7 épisodes)
├── 08_Bonus/          Hors-séries / formats courts
├── Assets/            Logos, polices, musiques, banque d'images
├── Templates/         Squelettes réutilisables (épisode, script, CSV)
└── Documentation/     Roadmap de saison
```

Chaque dossier d'épisode contient 8 étapes de production :
`01_Recherche → 02_Script → 03_Prompts_Images → 04_Miniature → 05_Metadata → 06_Audio → 07_Montage → 08_Publication`.

## Démarrage
1. Lire `00_Guidelines/` en entier.
2. Suivre `Documentation/Roadmap_Saison_01.md`.
3. Pour (re)générer la structure : `python init_project.py` (option `--force` pour réécrire les templates).

## Règle d'or
Aucune affirmation factuelle forte sans **≥ 2 sources indépendantes**, dont une universitaire ou primaire.
