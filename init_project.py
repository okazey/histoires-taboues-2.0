#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_project.py
===============
Script d'initialisation du projet documentaire YouTube
"Histoires Taboues - Résistance Africaine - Saison 01".

Ce script construit automatiquement :
  * l'arborescence complète des dossiers,
  * tous les fichiers modèles Markdown préremplis,
  * les fichiers CSV de prompts d'images (30 images par vidéo),
  * la documentation et la roadmap de saison.

Le projet est conçu comme un SYSTÈME DE PRODUCTION RÉUTILISABLE :
relancer ce script ne détruit rien (les fichiers existants sont préservés
par défaut ; utiliser --force pour réécrire les templates).

Usage :
    python init_project.py            # création / complétion non destructive
    python init_project.py --force    # réécrit tous les templates
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
#  CONFIGURATION GLOBALE
# --------------------------------------------------------------------------- #

ROOT_NAME = "Histoires_Taboues_Resistance_Africaine_Saison_01"
FORCE = "--force" in sys.argv

# Base = dossier où se trouve ce script (le dossier de travail de l'utilisateur)
BASE = Path(__file__).resolve().parent
ROOT = BASE / ROOT_NAME

# --------------------------------------------------------------------------- #
#  DONNÉES DES FIGURES HISTORIQUES (1 entrée par vidéo)
# --------------------------------------------------------------------------- #

VIDEOS = [
    {
        "slug": "01_Behanzin",
        "nom": "Béhanzin",
        "titre_complet": "Béhanzin, dernier roi indépendant du Dahomey",
        "region": "Royaume du Dahomey (actuel Bénin)",
        "periode": "1844 – 1906",
        "regne": "1889 – 1894",
        "ennemi": "France (conquête coloniale)",
        "conflit": "Guerres franco-dahoméennes (1890 et 1892-1894)",
        "fait_marquant": "Résistance armée appuyée sur le corps des Amazones du Dahomey ; "
                         "déportation en Martinique puis en Algérie.",
    },
    {
        "slug": "02_Lat_Dior",
        "nom": "Lat Dior Ngoné Latyr Diop",
        "titre_complet": "Lat Dior, Damel du Cayor",
        "region": "Royaume du Cayor (actuel Sénégal)",
        "periode": "1842 – 1886",
        "regne": "Damel du Cayor (par intermittence, 1862 – 1886)",
        "ennemi": "France (expansion coloniale, chemin de fer Dakar–Saint-Louis)",
        "conflit": "Résistance au tracé du chemin de fer ; bataille de Dékheulé (1886)",
        "fait_marquant": "Symbole de la résistance sénégalaise ; mort au combat à Dékheulé "
                         "avec son cheval Malaw.",
    },
    {
        "slug": "03_Menelik_II",
        "nom": "Ménélik II",
        "titre_complet": "Ménélik II, Empereur d'Éthiopie",
        "region": "Empire d'Éthiopie (Abyssinie)",
        "periode": "1844 – 1913",
        "regne": "Negusa Nagast (Roi des rois) 1889 – 1913",
        "ennemi": "Royaume d'Italie",
        "conflit": "Première guerre italo-éthiopienne ; bataille d'Adoua (1er mars 1896)",
        "fait_marquant": "Seule grande victoire africaine contre une puissance coloniale "
                         "européenne ayant garanti l'indépendance ; modernisation de l'État.",
    },
    {
        "slug": "04_Yaa_Asantewaa",
        "nom": "Yaa Asantewaa",
        "titre_complet": "Yaa Asantewaa, Reine-mère d'Ejisu",
        "region": "Empire Ashanti (actuel Ghana)",
        "periode": "v. 1840 – 1921",
        "regne": "Reine-mère (Ohemaa) d'Ejisu",
        "ennemi": "Empire britannique",
        "conflit": "Guerre du Trône d'or / Guerre des Ashanti (1900)",
        "fait_marquant": "A mené la dernière grande guerre ashanti contre les Britanniques ; "
                         "déportée aux Seychelles où elle meurt.",
    },
    {
        "slug": "05_El_Hadj_Omar_Tall",
        "nom": "El Hadj Omar Tall",
        "titre_complet": "El Hadj Omar Tall, fondateur de l'Empire toucouleur",
        "region": "Empire toucouleur (Sénégal, Mali, Guinée)",
        "periode": "v. 1797 – 1864",
        "regne": "Almami / chef de l'État toucouleur 1848 – 1864",
        "ennemi": "France (expansion sur le fleuve Sénégal) et États voisins",
        "conflit": "Djihad toucouleur ; siège de Médine (1857) face à Faidherbe",
        "fait_marquant": "Théoricien et chef d'un vaste État ouest-africain ; figure "
                         "religieuse et militaire majeure du XIXe siècle.",
    },
    {
        "slug": "06_Abdelkrim_El_Khattabi",
        "nom": "Abdelkrim El Khattabi",
        "titre_complet": "Mohamed Abdelkrim El Khattabi, émir du Rif",
        "region": "Rif (nord du Maroc)",
        "periode": "1882 – 1963",
        "regne": "Président de la République confédérée des tribus du Rif 1921 – 1926",
        "ennemi": "Espagne puis France",
        "conflit": "Guerre du Rif ; bataille d'Anoual (1921)",
        "fait_marquant": "Inflige à l'Espagne le désastre d'Anoual ; pionnier de la guérilla "
                         "moderne, source d'inspiration pour les mouvements anticoloniaux.",
    },
    {
        "slug": "07_Soundiata_Keita",
        "nom": "Soundiata Keïta",
        "titre_complet": "Soundiata Keïta, fondateur de l'Empire du Mali",
        "region": "Empire du Mali (Afrique de l'Ouest)",
        "periode": "v. 1190 – v. 1255",
        "regne": "Mansa (empereur) v. 1235 – v. 1255",
        "ennemi": "Royaume Sosso de Soumaoro Kanté",
        "conflit": "Bataille de Kirina (v. 1235)",
        "fait_marquant": "Fondateur de l'Empire du Mali et de la Charte du Manden (Kurukan Fuga), "
                         "l'une des plus anciennes déclarations de droits connues.",
    },
]

# Le dossier Bonus reçoit aussi la structure de production complète.
BONUS = {
    "slug": "08_Bonus",
    "nom": "Bonus / Hors-série",
    "titre_complet": "Épisode bonus — sujet transversal à définir",
    "region": "À définir",
    "periode": "À définir",
    "regne": "À définir",
    "ennemi": "À définir",
    "conflit": "À définir",
    "fait_marquant": "Réservé aux compilations, formats courts ou sujets transversaux "
                     "(les Amazones du Dahomey, la bataille d'Adoua, etc.).",
}

VIDEO_SUBFOLDERS = [
    "01_Recherche",
    "02_Script",
    "03_Prompts_Images",
    "04_Miniature",
    "05_Metadata",
    "06_Audio",
    "07_Montage",
    "08_Publication",
]

# --------------------------------------------------------------------------- #
#  OUTILS D'ÉCRITURE
# --------------------------------------------------------------------------- #

def write_file(path: Path, content: str) -> None:
    """Écrit un fichier texte sans écraser un fichier existant (sauf --force)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not FORCE:
        print(f"  = conservé : {path.relative_to(BASE)}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"  + écrit    : {path.relative_to(BASE)}")


def write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not FORCE:
        print(f"  = conservé : {path.relative_to(BASE)}")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  + écrit    : {path.relative_to(BASE)}")


# --------------------------------------------------------------------------- #
#  CONTENU : 00_GUIDELINES
# --------------------------------------------------------------------------- #

def guideline_ligne_editoriale() -> str:
    return """# Ligne Éditoriale — Histoires Taboues

> Document de référence. Toute vidéo de la chaîne doit respecter cette ligne.

## Mission de la chaîne

**« Raconter les histoires africaines que les manuels scolaires oublient. »**

Nous donnons une voix aux figures, aux royaumes et aux résistances que l'historiographie
dominante a marginalisés. Chaque épisode est un acte de mémoire rigoureux, jamais militant
au détriment des faits.

## Positionnement

La chaîne se concentre sur :

- **Résistance africaine** — rois, reines, chefs et peuples ayant tenu tête aux empires.
- **Colonisation** — mécanismes, acteurs, conséquences, sur le temps long.
- **Guerres oubliées** — batailles et campagnes absentes des programmes scolaires.
- **Figures historiques** — portraits incarnés, humains, documentés.
- **Crimes coloniaux** — exposés avec sources, sans complaisance ni surenchère.

## Promesse au spectateur

1. Une histoire vraie, sourcée, vérifiable.
2. Un récit incarné qui donne envie d'apprendre.
3. Une qualité de production constante (image, son, montage).
4. Le respect de la dignité des peuples et des personnes évoquées.

## Interdictions absolues

| Interdit | Pourquoi |
|----------|----------|
| **Fake history** | Détruit la crédibilité et trahit la mission. |
| **Révisionnisme** | Falsifier ou minimiser des faits établis est exclu. |
| **Sensationnalisme gratuit** | L'émotion sert le récit, jamais le clic seul. |
| **Sources non vérifiées** | Toute affirmation doit être étayée (voir Sources_*). |

## Règle d'or des sources

> Aucune affirmation factuelle forte n'entre dans un script sans **au moins deux sources
> indépendantes**, dont au moins une universitaire ou primaire.

<!-- COMMENTAIRE : compléter avec la charte de ton détaillée dans Style_Narratif.md -->
"""


def guideline_style_narratif() -> str:
    return """# Style Narratif — Histoires Taboues

> Comment on raconte. Le « comment » est aussi important que le « quoi ».

## Voix et posture

- Narrateur **incarné, grave et respectueux**, jamais neutre-froid ni sensationnaliste.
- On parle au spectateur comme à quelqu'un d'intelligent à qui l'on révèle une histoire cachée.
- Présent de narration pour les scènes-clés, passé pour le contexte.

## Principes d'écriture

1. **Montrer, pas asséner.** On plante une scène, un détail concret, un visage.
2. **Une idée par phrase.** Phrases courtes pour la tension, longues pour le contexte.
3. **Toujours nommer la source quand un fait est contesté** (« selon… », « les archives… »).
4. **Pas de jargon non expliqué.** Chaque terme historique est défini à la volée.
5. **Cliffhangers de chapitre.** Chaque section se termine sur une tension qui appelle la suite.

## Rythme

- **Hook (0:00–1:00)** : une scène forte, une question, un enjeu. Pas de logo interminable.
- **Montées et respirations** : alterner action et contexte pour éviter la saturation.
- **Climax** : la bataille / la chute, point émotionnel le plus haut.
- **Résolution** : héritage, écho contemporain, adresse finale au spectateur.

## Lexique à privilégier / à éviter

- ✅ « résistance », « souveraineté », « royaume », « archives », « témoignages ».
- ⚠️ Éviter « tribu » (préférer « peuple », « royaume », « confédération ») sauf citation sourcée.
- ❌ Bannir les formules racistes d'époque sauf en citation explicitement contextualisée.

## Gabarit d'un paragraphe de script

```
[VISUEL : description de l'image à l'écran]
[NARRATION : texte dit par la voix]
[NOTE PROD : musique / silence / effet]
```

<!-- COMMENTAIRE : adapter le niveau d'émotion selon la figure ; voir Script_Final.md de chaque épisode. -->
"""


def guideline_workflow() -> str:
    return """# Workflow de Production — Histoires Taboues

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
"""


def guideline_miniatures() -> str:
    return """# Règles des Miniatures (Thumbnails)

> La miniature décide 50 % du clic. Elle est traitée comme un livrable critique.

## Principes non négociables

1. **Un visage dominant** — émotion forte et lisible (regard, douleur, défi, fierté).
2. **Contraste élevé** — sujet détaché du fond, couleurs saturées maîtrisées.
3. **Texte ≤ 4 mots** — gros, lisible, sans empâtement.
4. **Lisible sur smartphone** — test obligatoire à la taille d'une vignette mobile.
5. **Cohérence de marque** — gabarit, police et bandeau identitaires constants.

## Check rapide avant validation

- [ ] Le visage exprime UNE émotion claire identifiable en 0,5 s.
- [ ] Le texte se lit à 5 cm de large (test mobile réel).
- [ ] Aucun élément essentiel dans les coins (zones masquées par l'UI YouTube).
- [ ] Contraste suffisant (test en niveaux de gris : le sujet reste lisible).
- [ ] Pas de promesse mensongère vs contenu (cohérent avec la ligne éditoriale).

## Gabarit recommandé

```
+------------------------------------------+
|  [VISAGE]                    TEXTE (≤4)   |
|  émotion forte               2 lignes max |
|  côté gauche ou centre       gros, jaune  |
|                              ou blanc     |
+------------------------------------------+
```

## Palette & typographie

- Couleur d'accent : _à définir_ (ex. or / rouge profond pour la résistance).
- Police titre : _à définir_ (graisse extra-bold, sans-serif condensé).

<!-- COMMENTAIRE : chaque épisode produit 2–3 variantes A/B dans 04_Miniature. -->
"""


def guideline_seo() -> str:
    return """# Règles SEO — Histoires Taboues

> Objectif : maximiser découvrabilité ET respect des faits. Pas de clickbait mensonger.

## Titre

- 60–70 caractères max ; le mot-clé fort en tête.
- Formule type : `NOM — l'histoire que les manuels ont effacée`.
- Une tension ou un enjeu, jamais une fausse promesse.

## Description

- **3 premières lignes = l'essentiel** (visibles sans « plus »).
- Résumé en 2–3 phrases + mots-clés naturels.
- Bloc chapitres (timestamps).
- Sources principales citées (crédibilité + valeur ajoutée).
- Liens, mentions, hashtags pertinents (3–5 max).

## Tags

- 15–25 tags : nom de la figure, royaume, pays, période, thèmes (résistance, colonisation…).
- Variantes orthographiques et langues (FR/EN) quand pertinent.

## Chapitres

- Calqués sur la structure narrative en 8 actes.
- Premier chapitre à 00:00 obligatoire.

## Bonnes pratiques

- Sous-titres (FR + EN) systématiques → portée + accessibilité.
- Vignette + titre testés ensemble (cohérence promesse/contenu).
- Commentaire épinglé : source clé ou question d'engagement.

<!-- COMMENTAIRE : remplir Titre.md / Description.md / Tags.md / Chapitres.md dans 05_Metadata de chaque épisode. -->
"""


def guideline_checklist_publication() -> str:
    return """# Checklist de Publication — Référence Chaîne

> Version maître. Chaque épisode duplique cette checklist dans `08_Publication/Publication_Checklist.md`.

## Avant mise en ligne

- [ ] **Miniature validée** (test mobile + A/B)
- [ ] **SEO validé** (titre, description, tags, chapitres — voir Regles_SEO.md)
- [ ] **Description validée** (3 premières lignes, sources, timestamps)
- [ ] **Tags validés** (15–25, pertinents)
- [ ] **Sous-titres générés** (FR + EN, relus)
- [ ] **Commentaires épinglés préparés** (source clé / question d'engagement)

## Contrôle qualité final

- [ ] Aucune affirmation non sourcée dans la vidéo.
- [ ] Crédits et sources affichés (fin de vidéo + description).
- [ ] Niveau audio normalisé (-14 LUFS cible YouTube).
- [ ] Vérification orthographe des cartons et sous-titres.
- [ ] Programmation à l'horaire de la roadmap (mardi / samedi 23h30).

## Après publication

- [ ] Épingler le commentaire.
- [ ] Vérifier l'affichage miniature/titre sur mobile et desktop.
- [ ] Partager sur les réseaux associés.
- [ ] Noter les premières métriques (CTR, rétention) pour itération.

<!-- COMMENTAIRE : ne rien publier tant qu'une case reste vide. -->
"""


# --------------------------------------------------------------------------- #
#  CONTENU : FICHIERS PAR VIDÉO
# --------------------------------------------------------------------------- #

def f_sources_primaires(v: dict) -> str:
    return f"""# Sources Primaires — {v['nom']}

> Documents d'époque : archives, correspondances, traités, témoignages directs, presse contemporaine.

## Fiche

- **Figure :** {v['titre_complet']}
- **Région :** {v['region']}
- **Période :** {v['periode']}

## Sources primaires identifiées

| # | Type | Référence / Cote | Dépôt / Accès | Fiabilité | Note |
|---|------|------------------|---------------|-----------|------|
| 1 | _archive_ | _placeholder_ | _placeholder_ | _à évaluer_ | _ex. correspondance militaire_ |
| 2 | _traité_ | _placeholder_ | _placeholder_ | _à évaluer_ | _ex. texte d'un traité_ |
| 3 | _témoignage_ | _placeholder_ | _placeholder_ | _à évaluer_ | _ex. récit d'un contemporain_ |
| 4 | _presse_ | _placeholder_ | _placeholder_ | _à évaluer_ | _ex. journal d'époque_ |

## À faire

- [ ] Identifier les fonds d'archives pertinents (nationales, militaires, missionnaires).
- [ ] Vérifier la provenance et le biais de chaque document.
- [ ] Numéroter les sources pour citation dans le script.

<!-- COMMENTAIRE : une source primaire ne vaut que reliée à son contexte ; noter les biais coloniaux des archives. -->
"""


def f_sources_universitaires(v: dict) -> str:
    return f"""# Sources Universitaires — {v['nom']}

> Travaux académiques : monographies, articles à comité de lecture, thèses, actes de colloque.

## Références (à compléter)

| # | Auteur·e | Titre | Année | Éditeur / Revue | Type | Note |
|---|----------|-------|-------|-----------------|------|------|
| 1 | _placeholder_ | _placeholder_ | _____ | _placeholder_ | monographie | _____ |
| 2 | _placeholder_ | _placeholder_ | _____ | _placeholder_ | article | _____ |
| 3 | _placeholder_ | _placeholder_ | _____ | _placeholder_ | thèse | _____ |

## Critères de sélection

- Priorité aux historiens spécialistes de {v['region']} et de la période ({v['periode']}).
- Croiser historiographie africaine et européenne ; signaler les désaccords.
- Distinguer faits établis, interprétations et débats ouverts.

## À faire

- [ ] Réunir ≥ 5 références académiques solides.
- [ ] Repérer les points de controverse entre historiens.
- [ ] Extraire citations exactes (avec page) pour le script.

<!-- COMMENTAIRE : noter explicitement les sujets où les sources divergent, pour éviter toute affirmation tranchée non fondée. -->
"""


def f_chronologie(v: dict) -> str:
    return f"""# Chronologie — {v['nom']}

> Frise factuelle. Chaque date doit être sourcée (renvoyer au numéro de Sources_*).

- **Figure :** {v['titre_complet']}
- **Période de vie :** {v['periode']}
- **Règne / action :** {v['regne']}
- **Adversaire principal :** {v['ennemi']}
- **Conflit central :** {v['conflit']}

## Frise

| Date | Événement | Lieu | Source(s) | Statut |
|------|-----------|------|-----------|--------|
| _____ | Naissance | _____ | _____ | à vérifier |
| _____ | Accession / début de l'action | _____ | _____ | à vérifier |
| _____ | Montée en puissance | _____ | _____ | à vérifier |
| _____ | Début du conflit | _____ | _____ | à vérifier |
| _____ | Bataille / tournant majeur | _____ | _____ | à vérifier |
| _____ | Chute / fin de la résistance | _____ | _____ | à vérifier |
| _____ | Décès | _____ | _____ | à vérifier |

## Fait marquant à mettre en avant

> {v['fait_marquant']}

<!-- COMMENTAIRE : signaler les dates incertaines (« v. » pour vers) ; ne jamais inventer une date précise. -->
"""


def f_personnages(v: dict) -> str:
    return f"""# Personnages — {v['nom']}

> Acteurs du récit : la figure centrale, alliés, adversaires, témoins.

## Figure centrale

- **Nom :** {v['titre_complet']}
- **Rôle :** {v['regne']}
- **Traits / caractère (sourcés) :** _placeholder_
- **Objectif / motivation :** _placeholder_

## Entourage et alliés

| Nom | Rôle | Relation | Note |
|-----|------|----------|------|
| _placeholder_ | _____ | allié | _____ |
| _placeholder_ | _____ | conseiller | _____ |

## Adversaires

| Nom | Camp | Rôle | Note |
|-----|------|------|------|
| _placeholder_ | {v['ennemi']} | commandant | _____ |
| _placeholder_ | {v['ennemi']} | administrateur | _____ |

## Témoins / voix secondaires

- _placeholder_ (utile pour incarner une scène ou citer un point de vue).

<!-- COMMENTAIRE : pour chaque personnage, une phrase de caractérisation sourcée suffit à l'incarner à l'écran. -->
"""


def f_bibliographie(v: dict) -> str:
    return f"""# Bibliographie — {v['nom']}

> Bibliographie consolidée et citable. Format conseillé : Auteur, *Titre*, Éditeur, Année.

## Ouvrages

1. _Auteur_, *Titre*, Éditeur, Année. — _note_
2. _Auteur_, *Titre*, Éditeur, Année. — _note_

## Articles & revues

1. _Auteur_, « Titre de l'article », *Revue*, vol., année, p. — _note_

## Sources en ligne (vérifiées)

1. _Institution / auteur_, « Titre », URL, consulté le ____. — _fiabilité_

## Ressources audiovisuelles / iconographiques

1. _placeholder_ (archives photo, gravures, cartes anciennes — vérifier droits).

## Suivi

- [ ] Toutes les sources du script figurent ici.
- [ ] Droits d'usage des images vérifiés.
- [ ] Bibliographie copiée dans la description (sélection) — voir 05_Metadata.

<!-- COMMENTAIRE : conserver une trace de chaque source consultée, même écartée, pour traçabilité. -->
"""


def f_script(v: dict, version: str) -> str:
    statut = {
        "V1": "Premier jet narratif. On cherche le souffle, pas la perfection.",
        "V2": "Version corrigée et sourcée. Vérifier chaque fait, ajouter les références.",
        "Final": "Version prête pour la voix. Verrouillée. Aucune affirmation non sourcée.",
    }[version]
    return f"""# Script {version} — {v['nom']}

> {statut}
>
> **Cible : 5500–6500 mots.** Durée visée : 25–30 min.
> Structure imposée en 8 actes (ne pas réordonner).

- **Figure :** {v['titre_complet']}
- **Conflit central :** {v['conflit']}
- **Adversaire :** {v['ennemi']}

---

## 1. Hook émotionnel  `[~0:00–1:00]`

[VISUEL : image choc d'ouverture]
[NARRATION : ouvrir sur une scène forte / une question. Donner immédiatement l'enjeu et
le mystère : pourquoi cette histoire a-t-elle été effacée ?]
[NOTE PROD : musique tendue, montée lente.]

<!-- Placeholder : 150–250 mots. -->

## 2. Contexte historique  `[~1:00–5:00]`

[NARRATION : situer {v['region']} à l'époque {v['periode']}. Le monde avant le conflit,
les forces en présence, l'équilibre menacé.]

<!-- Placeholder : 700–900 mots. -->

## 3. Ascension  `[~5:00–10:00]`

[NARRATION : montée en puissance de {v['nom']} ({v['regne']}). Décisions, alliances,
caractère. Donner chair au personnage.]

<!-- Placeholder : 900–1100 mots. -->

## 4. Guerre  `[~10:00–20:00]`

[NARRATION : le cœur du récit. {v['conflit']}. Tactiques, batailles, bascules, courage et pertes.]

<!-- Placeholder : 1400–1700 mots. -->

## 5. Contre-offensive coloniale  `[~20:00–24:00]`

[NARRATION : la riposte de {v['ennemi']}. Moyens, brutalité, rapport de force, tournant.]

<!-- Placeholder : 700–900 mots. -->

## 6. Chute  `[~24:00–27:00]`

[NARRATION : défaite, capture, exil ou mort. Le moment le plus grave. Respect et gravité.]

<!-- Placeholder : 500–700 mots. -->

## 7. Pourquoi il a été oublié  `[~27:00–28:30]`

[NARRATION : mécanismes de l'oubli — historiographie coloniale, silence des manuels,
effacement volontaire. Cœur de la mission de la chaîne.]

<!-- Placeholder : 400–600 mots. -->

## 8. Héritage  `[~28:30–30:00]`

[NARRATION : ce qu'il/elle laisse. Écho contemporain. Adresse finale au spectateur.]
[NOTE PROD : musique de clôture, fondu, carton sources.]

<!-- Placeholder : 300–500 mots. -->

---

### Contrôle final ({version})
- [ ] Total mots entre 5500 et 6500.
- [ ] Chaque fait fort renvoie à une source (Sources_Primaires / Universitaires).
- [ ] Ton conforme à Style_Narratif.md.
- [ ] Cliffhangers présents à chaque fin de section.
"""


def f_thumbnail_brief(v: dict) -> str:
    return f"""# Brief Miniature — {v['nom']}

> Voir 00_Guidelines/Regles_Miniatures.md pour les règles maîtres.

## Concept

- **Émotion principale :** _ex. défi / douleur / fierté_ (à choisir)
- **Message principal :** _l'angle de l'épisode en une idée_
- **Texte (≤ 4 mots) :** _placeholder_ (ex. « LE ROI OUBLIÉ »)

## Exigences visuelles

- [ ] **Visage dominant** ({v['nom']} ou symbole fort) au premier plan.
- [ ] **Contraste élevé** sujet / fond.
- [ ] **Lisible sur smartphone** (test vignette mobile réel).
- [ ] Cohérence de marque (gabarit, police, bandeau).

## Variantes à produire

| Variante | Émotion | Texte | Fond | Statut |
|----------|---------|-------|------|--------|
| A | _____ | _____ | _____ | à produire |
| B | _____ | _____ | _____ | à produire |
| C | _____ | _____ | _____ | optionnel |

## Décision

- Variante retenue : ____ — raison : ____ (idéalement après test A/B).

<!-- COMMENTAIRE : prompts d'images de miniature à dériver depuis 03_Prompts_Images si génération IA. -->
"""


def f_titre(v: dict) -> str:
    return f"""# Titre — {v['nom']}

> 60–70 caractères. Mot-clé fort en tête. Voir Regles_SEO.md.

## Propositions

1. {v['nom']} — l'histoire que les manuels ont effacée
2. {v['nom']} : {v['region'].split('(')[0].strip()} face à {v['ennemi'].split('(')[0].strip()}
3. _placeholder_ (angle émotion)
4. _placeholder_ (angle question)

## Titre retenu

> **_à choisir_**

- Caractères : ____ / 70
- Test mobile (troncature) : [ ] OK

<!-- COMMENTAIRE : éviter toute fausse promesse ; le titre doit tenir ce que la vidéo montre. -->
"""


def f_description(v: dict) -> str:
    return f"""# Description — {v['nom']}

> Les 3 premières lignes sont décisives (visibles sans « plus »).

## Accroche (3 lignes)

_placeholder accroche ligne 1 — l'enjeu._
_placeholder ligne 2 — la promesse._
_placeholder ligne 3 — l'appel à regarder._

## Corps

{v['titre_complet']} ({v['periode']}). Cet épisode retrace {v['conflit'].lower()} et
explique pourquoi cette histoire a été oubliée.

## Chapitres (timestamps)

00:00 Hook
01:00 Contexte historique
05:00 Ascension
10:00 Guerre
20:00 Contre-offensive coloniale
24:00 Chute
27:00 Pourquoi il/elle a été oublié·e
28:30 Héritage

## Sources principales

- _voir 01_Recherche/Bibliographie.md — citer 3 à 5 références clés._

## Liens & mentions

- Chaîne : _placeholder_
- Hashtags (3–5) : #HistoiresTaboues #RésistanceAfricaine #Histoire

<!-- COMMENTAIRE : recopier ici la sélection de sources finalisée avant publication. -->
"""


def f_tags(v: dict) -> str:
    pays = v["region"].split("(")[-1].replace(")", "").strip()
    return f"""# Tags — {v['nom']}

> 15–25 tags. Voir Regles_SEO.md.

## Liste (à affiner)

- {v['nom']}
- {v['titre_complet']}
- {v['region']}
- {pays}
- résistance africaine
- histoire africaine
- colonisation
- {v['ennemi'].split('(')[0].strip()}
- {v['conflit'].split('(')[0].strip()}
- guerres oubliées
- figures historiques
- crimes coloniaux
- Histoires Taboues
- documentaire histoire
- African history (EN)
- African resistance (EN)
- _placeholder variante orthographique_
- _placeholder période / siècle_

## Contrôle

- [ ] 15–25 tags.
- [ ] Variantes FR/EN incluses.
- [ ] Pas de tag hors-sujet (déréférencement YouTube).
"""


def f_chapitres(v: dict) -> str:
    return f"""# Chapitres — {v['nom']}

> Calqués sur la structure narrative. Premier chapitre à 00:00 obligatoire.

```
00:00 Hook
01:00 Contexte historique
05:00 Ascension
10:00 Guerre
20:00 Contre-offensive coloniale
24:00 Chute
27:00 Pourquoi il/elle a été oublié·e
28:30 Héritage
```

## À ajuster après montage

- [ ] Timestamps recalés sur le montage final (07_Montage/Timeline.md).
- [ ] Libellés courts et clairs.
- [ ] Copiés dans Description.md.
"""


def f_narration(v: dict) -> str:
    return f"""# Narration — {v['nom']}

> Brief voix : ton, rythme, prononciations.

## Direction de voix

- Ton : grave, incarné, respectueux (voir Style_Narratif.md).
- Débit : posé sur le contexte, plus tendu sur les batailles.
- Respiration : marquer les silences avant les moments forts.

## Lexique & prononciation

| Mot / nom | Prononciation | Note |
|-----------|---------------|------|
| {v['nom']} | _placeholder_ | respecter la prononciation locale |
| _toponyme_ | _placeholder_ | _____ |

## Production

- [ ] Voix : humaine / synthèse (préciser l'outil et la licence).
- [ ] Fichier(s) audio nommés `narration_<chapitre>.wav`.
- [ ] Niveau cible -16 LUFS voix seule (mix final -14 LUFS).

<!-- COMMENTAIRE : fournir au comédien/à l'outil les prononciations validées avant enregistrement. -->
"""


def f_prompt_musique(v: dict) -> str:
    return f"""# Brief Musique — {v['nom']}

> Pour compositeur, banque de musique ou génération IA. Vérifier les licences.

## Intentions par section

| Section | Ambiance | Instruments / texture | Intensité |
|---------|----------|-----------------------|-----------|
| Hook | tension, mystère | nappes graves, percussions lointaines | montante |
| Contexte | ample, narratif | cordes, instruments traditionnels {v['region'].split('(')[0].strip()} | moyenne |
| Ascension | espoir, élan | percussions, montée rythmique | montante |
| Guerre | épique, sombre | tambours, cuivres, choeurs | haute |
| Chute | tragique, recueilli | cordes solo, silence | basse |
| Héritage | mémoire, lumière | thème principal réorchestré | moyenne |

## Prompt génératif (exemple)

> « Cinematic historical documentary score, West/North African traditional
> instruments blended with orchestral strings and deep drums, solemn and epic,
> evolving from tension to tragedy to remembrance. »  <!-- adapter à {v['nom']} -->

## Contrôle

- [ ] Licences libres de droits vérifiées.
- [ ] Thème principal identifiable et récurrent.
- [ ] Pas de saturation sous la narration (ducking).
"""


def f_effets_sonores(v: dict) -> str:
    return f"""# Effets Sonores (SFX) — {v['nom']}

> Liste des ambiances et bruitages, avec sources libres de droits.

## Banque de SFX

| Scène | Effet | Source | Licence | Statut |
|-------|-------|--------|---------|--------|
| Bataille | foule, armes, chevaux | _placeholder_ | _____ | à sourcer |
| Cour royale | ambiance, voix lointaines | _placeholder_ | _____ | à sourcer |
| Nature / région | vent, faune, eau | _placeholder_ | _____ | à sourcer |
| Transitions | impacts, whoosh | _placeholder_ | _____ | à sourcer |

## Règles

- [ ] Cohérence historique et géographique (pas d'anachronisme sonore).
- [ ] Niveaux discrets, jamais au-dessus de la voix.
- [ ] Sources et licences notées pour la traçabilité.
"""


def f_storyboard(v: dict) -> str:
    return f"""# Storyboard — {v['nom']}

> Plan par plan : ce que voit le spectateur, en regard du script.

## Gabarit

| Plan | Section script | Visuel (image/scène) | Texte à l'écran | Son / musique | Durée |
|------|----------------|----------------------|-----------------|---------------|-------|
| 001 | Hook | _image_ | _carton_ | tension | 00:08 |
| 002 | Hook | _image_ | — | — | 00:06 |
| ... | ... | ... | ... | ... | ... |

## Principes

- Une image neuve toutes les ~6–10 s minimum (rythme visuel).
- Cartes pour situer la géographie ({v['region']}).
- Cartons de date sobres et cohérents.

<!-- COMMENTAIRE : relier chaque plan à une ligne de prompts_images.csv (Scene_ID). -->
"""


def f_timeline(v: dict) -> str:
    return f"""# Timeline — {v['nom']}

> Découpage temporel cible (à recaler sur le montage final).

```
00:00  Hook
01:00  Contexte
05:00  Ascension
10:00  Guerre
20:00  Chute
27:00  Héritage
```

## Détail des blocs

| Début | Bloc | Contenu | Notes montage |
|-------|------|---------|---------------|
| 00:00 | Hook | scène d'ouverture | musique tendue |
| 01:00 | Contexte | mise en situation | cartes |
| 05:00 | Ascension | montée de {v['nom']} | rythme croissant |
| 10:00 | Guerre | {v['conflit'].split('(')[0].strip()} | climax sonore |
| 20:00 | Chute | défaite / exil | ralenti, gravité |
| 27:00 | Héritage | mémoire, écho | clôture |

## Contrôle

- [ ] Durée totale 25–30 min.
- [ ] Timestamps reportés dans Chapitres.md / Description.md.
- [ ] Rétention : pas de creux > 20 s sans relance visuelle/sonore.
"""


def f_publication_checklist(v: dict) -> str:
    return f"""# Checklist de Publication — {v['nom']}

> Dupliquée depuis 00_Guidelines/Checklist_Publication.md. Rien ne sort sans tout coché.

## Validation contenu

- [ ] Miniature validée (test mobile + A/B)
- [ ] SEO validé (titre, description, tags, chapitres)
- [ ] Description validée (3 premières lignes, sources, timestamps)
- [ ] Tags validés (15–25)
- [ ] Sous-titres générés (FR + EN, relus)
- [ ] Commentaires épinglés préparés

## Qualité finale

- [ ] Aucune affirmation non sourcée
- [ ] Crédits / sources affichés (vidéo + description)
- [ ] Audio normalisé (-14 LUFS)
- [ ] Orthographe cartons & sous-titres vérifiée
- [ ] Programmation à l'horaire roadmap (mardi / samedi 23h30)

## Après publication

- [ ] Commentaire épinglé
- [ ] Affichage miniature/titre vérifié (mobile + desktop)
- [ ] Partage réseaux
- [ ] Métriques notées (CTR, rétention) pour itération

---
**Épisode :** {v['titre_complet']}
**Statut global :** ⬜ Brouillon · ⬜ Prêt · ⬜ Publié
"""


# --------------------------------------------------------------------------- #
#  CSV DES PROMPTS D'IMAGES (30 lignes)
# --------------------------------------------------------------------------- #

def build_prompts_rows(v: dict) -> list[list[str]]:
    """Génère 30 lignes : 10 portraits, 10 scènes, 5 cartes, 5 émotionnelles."""
    nom = v["nom"]
    region = v["region"].split("(")[0].strip()
    rows: list[list[str]] = []

    chapitres_cycle = [
        "Hook", "Contexte", "Ascension", "Guerre",
        "Contre-offensive", "Chute", "Oubli", "Héritage",
    ]

    def whisk(desc: str) -> str:
        return (f"Cinematic historical portrait/scene, {desc}, {region}, 19th-century "
                f"documentary realism, dramatic lighting, high detail, photorealistic, --ar 16:9")

    def flow(desc: str) -> str:
        return (f"{desc}. Style: epic historical documentary, volumetric light, "
                f"muted earthy palette, motion-ready composition, 16:9")

    def mj(desc: str) -> str:
        return (f"{desc}, historical documentary, cinematic lighting, ultra detailed, "
                f"35mm film, dramatic mood --ar 16:9 --style raw")

    # 10 portraits
    portrait_descs = [
        f"{nom}, close-up face, intense determined gaze",
        f"{nom} in royal/traditional regalia, half body",
        f"{nom} as a young leader, hopeful expression",
        f"{nom} in council with advisors",
        f"{nom} in war attire before battle",
        f"{nom}, weary after defeat, dignified",
        f"{nom} portrait in profile, symbolic",
        f"a key ally of {nom}, supporting figure",
        f"the main adversary facing {nom}",
        f"{nom} elder/in exile, reflective",
    ]
    for i, d in enumerate(portrait_descs, start=1):
        ch = chapitres_cycle[(i - 1) % len(chapitres_cycle)]
        rows.append([f"P{i:02d}", ch, f"Portrait — {d}", whisk(d), flow(d), mj(d)])

    # 10 scènes historiques
    scene_descs = [
        f"royal court of {region}, ceremony",
        f"daily life in {region} before the war",
        f"army of {nom} marching",
        f"major battle of the conflict, chaos and smoke",
        f"colonial troops advancing with artillery",
        f"siege / fortified position under attack",
        f"negotiation or tense diplomatic meeting",
        f"village burning, aftermath of an assault",
        f"capture or surrender scene, solemn",
        f"exile / deportation by ship or convoy",
    ]
    for i, d in enumerate(scene_descs, start=1):
        ch = chapitres_cycle[(i + 1) % len(chapitres_cycle)]
        rows.append([f"S{i:02d}", ch, f"Scène historique — {d}", whisk(d), flow(d), mj(d)])

    # 5 cartes
    map_descs = [
        f"map of {region} showing the kingdom at its height",
        f"map of military campaign routes and battles",
        f"map of colonial expansion pressing the borders",
        f"map locating the decisive battle site",
        f"map of exile route / final territory loss",
    ]
    for i, d in enumerate(map_descs, start=1):
        ch = chapitres_cycle[i % len(chapitres_cycle)]
        prompt = (f"Antique-style historical map, {d}, parchment texture, labeled, "
                  f"muted tones, documentary infographic, 16:9")
        rows.append([f"C{i:02d}", ch, f"Carte — {d}", prompt, flow(d), mj(d + ", antique map style")])

    # 5 images émotionnelles
    emo_descs = [
        "tearful close-up, grief of a people",
        "child watching the war from afar, fear",
        "broken crown / symbol of a fallen kingdom",
        "hands in chains, loss of freedom",
        "candle / memory, remembrance and legacy",
    ]
    for i, d in enumerate(emo_descs, start=1):
        ch = ["Chute", "Guerre", "Chute", "Oubli", "Héritage"][i - 1]
        rows.append([f"E{i:02d}", ch, f"Image émotionnelle — {d}", whisk(d), flow(d), mj(d)])

    return rows


# --------------------------------------------------------------------------- #
#  TEMPLATES & DOCUMENTATION
# --------------------------------------------------------------------------- #

def template_episode_readme() -> str:
    return """# Template Épisode — Mode d'emploi

> Copier ce squelette pour tout nouvel épisode. La structure interne est générée
> par `init_project.py` mais ce template documente l'usage de chaque dossier.

```
NN_Nom_Figure/
├── 01_Recherche/      Sources_Primaires, Sources_Universitaires, Chronologie, Personnages, Bibliographie
├── 02_Script/         Script_V1, Script_V2, Script_Final (5500–6500 mots, 8 actes)
├── 03_Prompts_Images/ prompts_images.csv (30 images)
├── 04_Miniature/      thumbnail_brief.md
├── 05_Metadata/       Titre, Description, Tags, Chapitres
├── 06_Audio/          Narration, Prompt_Musique, Effets_Sonores
├── 07_Montage/        Storyboard, Timeline
└── 08_Publication/    Publication_Checklist
```

## Ordre de travail
1. Recherche → 2. Script → 3. Prompts → 4. Miniature → 5. Metadata → 6. Audio → 7. Montage → 8. Publication
"""


def template_csv_header_doc() -> str:
    return """# Template — prompts_images.csv

Colonnes :

| Colonne | Sens |
|---------|------|
| Scene_ID | Identifiant (P=portrait, S=scène, C=carte, E=émotion) |
| Chapitre | Section narrative associée |
| Description | Ce que montre l'image |
| Prompt_Whisk | Prompt pour Whisk |
| Prompt_Flow | Prompt pour Flow |
| Prompt_Midjourney | Prompt pour Midjourney |

Répartition imposée des 30 images : 10 portraits, 10 scènes historiques, 5 cartes, 5 images émotionnelles.
"""


def template_script_skeleton() -> str:
    return """# Template — Squelette de Script (8 actes)

1. **Hook émotionnel** — scène/question d'ouverture, enjeu immédiat.
2. **Contexte historique** — le monde avant.
3. **Ascension** — montée du personnage.
4. **Guerre** — cœur du récit.
5. **Contre-offensive coloniale** — la riposte.
6. **Chute** — défaite / exil / mort.
7. **Pourquoi il a été oublié** — mécanismes de l'oubli.
8. **Héritage** — écho contemporain.

Cible : **5500–6500 mots**. Format de paragraphe : `[VISUEL]` / `[NARRATION]` / `[NOTE PROD]`.
"""


def doc_roadmap() -> str:
    lignes = "\n".join(
        f"| {i} | {v['nom']} | {v['titre_complet']} | ⬜ |"
        for i, v in enumerate(
            [VIDEOS[0], VIDEOS[1], VIDEOS[2], VIDEOS[3], VIDEOS[4], VIDEOS[5], VIDEOS[6]],
            start=1,
        )
    )
    return f"""# Roadmap — Saison 01 : Résistance Africaine

> Plan de production et calendrier de publication.

## Rythme de publication

- **Mardi 23h30**
- **Samedi 23h30**

Deux vidéos par semaine. Chaque épisode suit le workflow en 8 étapes
(voir 00_Guidelines/Workflow_Production.md).

## Ordre de la saison

| # | Figure | Épisode | Statut |
|---|--------|---------|--------|
{lignes}

## Calendrier (à dater)

| Créneau | Date | Épisode | Statut prod |
|---------|------|---------|-------------|
| Mardi 23h30 | ____ | 1. Béhanzin | ⬜ Recherche |
| Samedi 23h30 | ____ | 2. Lat Dior | ⬜ Recherche |
| Mardi 23h30 | ____ | 3. Ménélik II | ⬜ |
| Samedi 23h30 | ____ | 4. Yaa Asantewaa | ⬜ |
| Mardi 23h30 | ____ | 5. El Hadj Omar Tall | ⬜ |
| Samedi 23h30 | ____ | 6. Abdelkrim El Khattabi | ⬜ |
| Mardi 23h30 | ____ | 7. Soundiata Keïta | ⬜ |

## Suivi d'avancement (légende)
⬜ À faire · 🟦 En cours · ✅ Terminé

## Bonus
Le dossier `08_Bonus` accueille hors-séries et formats courts (voir sa structure dédiée).

<!-- COMMENTAIRE : dater les créneaux dès le lancement ; ne pas publier un épisode dont la checklist n'est pas complète. -->
"""


def root_readme() -> str:
    return f"""# {ROOT_NAME}

Système de production documentaire pour la chaîne YouTube **Histoires Taboues**.
Saison 01 — **Résistance Africaine**.

## Mission
> « Raconter les histoires africaines que les manuels scolaires oublient. »

## Arborescence
```
{ROOT_NAME}/
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
"""


def assets_readme() -> str:
    return """# Assets

Ressources partagées de la chaîne.

```
Assets/
├── Logos/        logo chaîne, watermark
├── Polices/      typographies titres & cartons (vérifier licences)
├── Musiques/     pistes libres de droits (par ambiance)
├── SFX/          bruitages libres de droits
├── Images/       banque d'images générées / archives (droits vérifiés)
└── Cartes/       fonds de cartes réutilisables
```

<!-- COMMENTAIRE : noter la licence de chaque asset dans un fichier LICENCES.md à créer ici. -->
"""


# --------------------------------------------------------------------------- #
#  CONSTRUCTION
# --------------------------------------------------------------------------- #

def build_guidelines() -> None:
    g = ROOT / "00_Guidelines"
    write_file(g / "Ligne_Editoriale.md", guideline_ligne_editoriale())
    write_file(g / "Style_Narratif.md", guideline_style_narratif())
    write_file(g / "Workflow_Production.md", guideline_workflow())
    write_file(g / "Regles_Miniatures.md", guideline_miniatures())
    write_file(g / "Regles_SEO.md", guideline_seo())
    write_file(g / "Checklist_Publication.md", guideline_checklist_publication())


def build_video(v: dict) -> None:
    base = ROOT / v["slug"]

    # 01_Recherche
    r = base / "01_Recherche"
    write_file(r / "Sources_Primaires.md", f_sources_primaires(v))
    write_file(r / "Sources_Universitaires.md", f_sources_universitaires(v))
    write_file(r / "Chronologie.md", f_chronologie(v))
    write_file(r / "Personnages.md", f_personnages(v))
    write_file(r / "Bibliographie.md", f_bibliographie(v))

    # 02_Script
    s = base / "02_Script"
    write_file(s / "Script_V1.md", f_script(v, "V1"))
    write_file(s / "Script_V2.md", f_script(v, "V2"))
    write_file(s / "Script_Final.md", f_script(v, "Final"))

    # 03_Prompts_Images
    p = base / "03_Prompts_Images"
    write_csv(
        p / "prompts_images.csv",
        ["Scene_ID", "Chapitre", "Description", "Prompt_Whisk", "Prompt_Flow", "Prompt_Midjourney"],
        build_prompts_rows(v),
    )

    # 04_Miniature
    write_file(base / "04_Miniature" / "thumbnail_brief.md", f_thumbnail_brief(v))

    # 05_Metadata
    m = base / "05_Metadata"
    write_file(m / "Titre.md", f_titre(v))
    write_file(m / "Description.md", f_description(v))
    write_file(m / "Tags.md", f_tags(v))
    write_file(m / "Chapitres.md", f_chapitres(v))

    # 06_Audio
    a = base / "06_Audio"
    write_file(a / "Narration.md", f_narration(v))
    write_file(a / "Prompt_Musique.md", f_prompt_musique(v))
    write_file(a / "Effets_Sonores.md", f_effets_sonores(v))

    # 07_Montage
    mo = base / "07_Montage"
    write_file(mo / "Storyboard.md", f_storyboard(v))
    write_file(mo / "Timeline.md", f_timeline(v))

    # 08_Publication
    write_file(base / "08_Publication" / "Publication_Checklist.md", f_publication_checklist(v))


def build_templates() -> None:
    t = ROOT / "Templates"
    write_file(t / "README_Template_Episode.md", template_episode_readme())
    write_file(t / "Template_Script_8_Actes.md", template_script_skeleton())
    write_file(t / "Template_prompts_images.md", template_csv_header_doc())


def build_assets() -> None:
    a = ROOT / "Assets"
    for sub in ["Logos", "Polices", "Musiques", "SFX", "Images", "Cartes"]:
        (a / sub).mkdir(parents=True, exist_ok=True)
    write_file(a / "README.md", assets_readme())


def build_documentation() -> None:
    d = ROOT / "Documentation"
    write_file(d / "Roadmap_Saison_01.md", doc_roadmap())


def main() -> None:
    print(f"Initialisation du projet : {ROOT_NAME}")
    print(f"Emplacement : {ROOT}")
    print(f"Mode : {'FORCE (réécriture)' if FORCE else 'non destructif'}\n")

    ROOT.mkdir(parents=True, exist_ok=True)

    write_file(ROOT / "README.md", root_readme())

    print("\n[00_Guidelines]")
    build_guidelines()

    for v in VIDEOS + [BONUS]:
        print(f"\n[{v['slug']}]")
        build_video(v)

    print("\n[Assets]")
    build_assets()
    print("\n[Templates]")
    build_templates()
    print("\n[Documentation]")
    build_documentation()

    print("\n✅ Projet généré avec succès.")


if __name__ == "__main__":
    main()
