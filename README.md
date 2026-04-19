# Projet ecommerce — Nettoyage & Analyse

Pipeline de nettoyage de données de ventes avec `pandas`, suivi d'une analyse du chiffre d'affaires et d'une visualisation interactive.

---

## Structure du projet

```
projet-ventes/
├── README.md                          ← Ce fichier
├── .gitignore
├── data/
│   ├── ventes.csv                     ← Dataset brut (raw)
│   └── ventes_clean.csv               ← Dataset nettoyé, prêt pour analyse
└── notebooks/
    ├── nettoyage_ventes.ipynb         ← Pipeline de nettoyage des données
    ├── analyse_ca.ipynb               ← Analyse du chiffre d'affaires
    │                                     • Étape 2 : Calcul CA Brut (Prix × Quantité)
    │                                     • Étape 3 : Calcul CA Net (après remises)
    │                                     • Étape 4 : Calcul TVA (20% sur CA Net)
    │                                     • Étape 5 : CA Total de l'entreprise
    │                                     • Étape 6 : Produit avec le plus gros CA Net
    │                                     • Étape 7 : Export resultats_final.csv
    └── visualisation_ca.ipynb         ← Visualisation interactive du CA par produit
                                          • Graphique 1 : CA Total par produit (barres)
                                          • Graphique 2 : CA Brut vs CA Net (remises)
                                          • Graphique 3 : TVA collectée par produit
                                          • Graphique 4 : Scatter CA Net vs TVA
                                          • Graphique 5 : Dashboard récapitulatif 4-en-1
                                          • Export : dashboard_ca.html (interactif)
```

---

## Objectif

Partir d'un jeu de données de ventes contenant des incohérences réalistes (valeurs manquantes, formats mixtes, doublons, outliers), le nettoyer, calculer et analyser le chiffre d'affaires, puis le visualiser de manière interactive.

---

## Description des données

Le fichier `ventes.csv` contient 100 transactions avec les colonnes suivantes :

| Colonne    | Type attendu | Description                         |
|------------|--------------|-------------------------------------|
| `ID`       | int          | Identifiant unique de la transaction |
| `Prix`     | float        | Prix unitaire en euros              |
| `Quantite` | int          | Nombre d'unités vendues             |
| `Remise`   | float        | Pourcentage de remise (0–100)       |

Le fichier `resultats_final.csv` (produit par `analyse_ca.ipynb`) contient les colonnes calculées :

| Colonne    | Type     | Description                         |
|------------|----------|-------------------------------------|
| `ID`       | int      | Identifiant unique de la transaction |
| `Prix`     | float    | Prix unitaire en euros              |
| `Quantite` | int      | Nombre d'unités vendues             |
| `Remise`   | float    | Pourcentage de remise (0–100)       |
| `CA_Brut`  | float    | Chiffre d'affaires brut (€)         |
| `CA_Net`   | float    | Chiffre d'affaires après remise (€) |
| `TVA`      | float    | TVA collectée à 20% (€)            |
| `CA_Total` | float    | CA Net + TVA (€)                    |

### Problèmes présents dans les données brutes

- **Valeurs manquantes** sur les trois colonnes numériques
- **Formats mixtes** : virgules décimales à la française (`50,37`), symbole `€`, symbole `%`
- **Valeurs textuelles** dans `Quantite` (`"cinq"`, `"deux"`)
- **Valeurs aberrantes** : prix négatifs, remises > 100%, quantités extrêmes
- **IDs dupliqués**

---

## Règles de nettoyage appliquées

| Colonne    | Traitement |
|------------|-----------|
| `Prix`     | Suppression du `€`, virgule → point, conversion en float, prix négatifs → valeur absolue |
| `Quantite` | Conversion des nombres en lettres (`"cinq"` → `5`), conversion en int |
| `Remise`   | Suppression du `%`, conversion en float, valeurs hors [0, 100] → NaN |
| `ID`       | Suppression des doublons (première occurrence conservée) |

### Imputation des valeurs manquantes
- `Prix` et `Quantite` → **médiane** de la colonne
- `Remise` → **0** (pas de remise par défaut)

---

## Visualisations

Le notebook `visualisation_ca.ipynb` génère 5 graphiques interactifs avec **Plotly** à partir de `resultats_final.csv` :

| Graphique | Type | Description |
|-----------|------|-------------|
| CA Total par produit | Barres verticales | Comparaison du CA total, trié du plus grand au plus petit |
| CA Brut vs CA Net | Barres empilées | Impact des remises sur le CA |
| TVA collectée | Barres horizontales | TVA par produit triée croissante |
| Scatter CA Net / TVA | Nuage de points | Relation entre CA net et TVA, taille = quantité, couleur = remise |
| Dashboard 4-en-1 | Subplots | Vue d'ensemble : camembert, scatter prix/qté, histogramme remises, CA Net vs TVA |

Le résultat final est exporté en `dashboard_ca.html` — fichier autonome, ouvrable dans n'importe quel navigateur sans installation.

---

## Démarrage rapide

### Prérequis

```bash
pip install pandas numpy jupyter plotly
```

### Cloner le projet

```bash
git clone https://github.com/<ton-user>/projet-ventes.git
cd projet-ventes
```

### Charger le dataset propre

```python
import pandas as pd
df = pd.read_csv('data/ventes_clean.csv')
df.head()
```

### Lancer les visualisations

```python
# Dans le notebook visualisation_ca.ipynb
# Adapter le chemin du fichier dans la cellule 3 :
df = pd.read_csv('resultats_final.csv')
```

---

## Workflow

1. **Cellule 1** du notebook `nettoyage_ventes.ipynb` génère `ventes.csv` (dataset sale)
2. **Cellules 2 à 10** nettoient les données et exportent `ventes_clean.csv`
3. Le notebook `analyse_ca.ipynb` consomme `ventes_clean.csv` pour les calculs métier et exporte `resultats_final.csv`
4. Le notebook `visualisation_ca.ipynb` consomme `resultats_final.csv` et génère `dashboard_ca.html`

---

## Équipe & répartition

| Membre | Responsabilité |
|--------|----------------|
| **Rania Doghri** | Génération du dataset & pipeline de nettoyage |
| **May Ouni** | Conception du script Python, calcul des indicateurs financiers, interprétation des résultats et export des données |
| **Nour el houda Limame** | Visualisation du CA par produit — graphiques interactifs avec Plotly (barres, scatter, dashboard 4-en-1) et export HTML |

---

## Conventions Git

- Travailler sur des branches dédiées : `feature/nettoyage`, `feature/analyse-ca`, `feature/visualisation`
- Messages de commit en français, format court : `ajout`, `fix`, `refacto`, `docs`
- Ouvrir une Pull Request avant de merger sur `main`

---

## Notes techniques

- Encodage des fichiers CSV : **UTF-8**
- Séparateur : **virgule** (`,`)
- Python ≥ 3.10 recommandé
- Les graphiques Plotly nécessitent `plotly` installé (`pip install plotly`)
- L'export PNG nécessite `kaleido` (`pip install kaleido`) — l'export HTML fonctionne sans
- pip install matplotlib pandas NumPy
- pip install plotly pandas openpyxl
- pip install plotly pandas

---

## Licence

Projet PFA
