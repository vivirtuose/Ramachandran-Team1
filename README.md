# Ramachandran-Team1

Projet de programmation orientée objet (Master 2 Bioinformatique) : construire, à
plusieurs, une chaîne complète qui va d'un fichier de structure 3D de protéine (PDB)
jusqu'à la classification des angles du squelette peptidique dans le diagramme de
Ramachandran.

## Objectifs du projet

La conformation du squelette d'une protéine est décrite par deux angles dièdres par
résidu : **φ (phi)**, la torsion autour de la liaison N–Cα, et **ψ (psi)**, la torsion
autour de la liaison Cα–C. Toutes les combinaisons (φ, ψ) ne sont pas possibles, à
cause de l'encombrement stérique. Représentés dans le plan, les couples (φ, ψ) d'une
protéine se regroupent en zones, qui correspondent aux structures secondaires
(hélices, feuillets, boucles).

Le projet réalise les étapes suivantes :

1. **Lire** un fichier PDB et en extraire les atomes du squelette (N, CA, C, O).
2. **Organiser** ces atomes en acides aminés, puis en une structure de protéine.
3. **Calculer** les angles dièdres φ et ψ de chaque résidu, et en faire des points du
   plan (le diagramme de Ramachandran).
4. **Clusteriser** ces points avec deux algorithmes (K-means et DBSCAN) pour repérer
   les zones d'hélices, de feuillets et de boucles.
5. **Mesurer la qualité** d'un clustering (coefficient de silhouette, indice de Dunn).
6. **Tester** chaque classe avec des tests unitaires (module `unittest`), y compris sur
   les cas limites.

## Architecture du dépôt

```
Ramachandran-Team1/
├── 1.ATOM_AMINO/        Briques de base : atomes et acides aminés
│   ├── Atom.py
│   └── AminoAcid.py
├── 2.PDB_STRUCT/        Lecture du PDB et calcul des angles
│   ├── PDBStructure.py
│   ├── Point.py
│   └── 1TEY.pdb
├── 3.STATS/             Clustering et mesures de qualité
│   ├── clustering.py
│   ├── clusteringMeasures.py
│   └── angle_1TEY_small_clust.txt
├── 4.TEST/              Tests unitaires et tests d'usage
│   ├── test_Atom.py
│   ├── test_AminoAcid.py
│   ├── test_point.py
│   ├── test_pdbstructure.py
│   ├── test_ClusterPoint.py
│   ├── test_ClusteringMethods.py
│   ├── test_Kmeans.py
│   ├── test_DBscans.py
│   ├── test_ClusteringMeasures.py
│   └── archive/
├── 1TEY.pdb             Fichier PDB complet (structure résolue par RMN)
└── 1tey_model1.pdb      Premier modèle de 1TEY (156 résidus), utilisé pour les tests
```

### 1.ATOM_AMINO

| Script | Classe | Rôle |
|---|---|---|
| `Atom.py` | `Atom` | Un atome (nom et coordonnées x, y, z). Calculs géométriques : norme, distance, soustraction, produit scalaire, produit vectoriel, angle entre deux vecteurs, angle dièdre. |
| `AminoAcid.py` | `AminoAcid` | Un acide aminé : numéro, type (MET, ALA...) et atomes du squelette. Accès aux atomes N, CA, C et O, et ajout d'un atome. |

### 2.PDB_STRUCT

| Script | Classe | Rôle |
|---|---|---|
| `PDBStructure.py` | `StructurePDB` | Lit un fichier PDB, construit la liste des acides aminés, calcule les angles dièdres φ et ψ (`compute_dihedrals`) et les écrit dans un fichier (`write_dihedrals`). |
| `Point.py` | `Point` | Un point du plan (abscisse, ordonnée) : addition, mise à l'échelle, distance à l'origine, distance euclidienne et distance de Manhattan. Un point (φ, ψ) est un `Point`. |

### 3.STATS

| Script | Classes | Rôle |
|---|---|---|
| `clustering.py` | `ClusterPoint`, `ClusteringMethods`, `Kmeans`, `dbscan` | `ClusterPoint` est un `Point` qui porte en plus un numéro de cluster. `ClusteringMethods` est la classe abstraite commune. `Kmeans` regroupe les points autour de k centroïdes. `dbscan` regroupe les points selon leur densité et laisse les points isolés en dehors des clusters (bruit). Les résultats peuvent s'exporter en fichier tabulé à trois colonnes (phi, psi, cluster). |
| `clusteringMeasures.py` | `ClusteringMeasures` | Mesures de qualité d'un clustering : coefficient de silhouette et indice de Dunn. Se construit à partir d'une liste de `ClusterPoint` ou d'un fichier tabulé. |
| `angle_1TEY_small_clust.txt` | | Petit fichier d'exemple : un point par ligne, avec phi, psi et le numéro de cluster séparés par des tabulations. |

### 4.TEST

Un fichier de test par classe, écrit avec `unittest`. Les tests couvrent le
fonctionnement normal, les cas limites (listes vides, paramètres invalides, fichiers mal
formés) et quelques cas d'usage dont la réponse est connue à l'avance. Le dossier
`archive/` garde d'anciennes versions de travail.

## Résultats attendus

Sur `1tey_model1.pdb` (156 résidus), le code doit produire :

- **154 couples (φ, ψ)**, en radians. Le premier résidu n'a pas de φ et le dernier n'a
  pas de ψ.
- Pour les premiers résidus, les valeurs suivantes :

  | phi | psi |
  |---|---|
  | -1.296614 | 2.370531 |
  | -1.511338 | -0.570213 |
  | -2.371938 | 2.313760 |
  | -2.258944 | 1.963503 |
  | -1.259170 | 2.105960 |

- Un **fichier tabulé** de ces angles (méthode `write_dihedrals`), exploitable pour
  tracer le diagramme de Ramachandran.
- Un **clustering** de ces points : avec K-means, k groupes qui se partagent tous les
  points ; avec DBSCAN, des clusters denses et un reste de points isolés. Les groupes
  obtenus doivent correspondre aux grandes zones du diagramme (hélices, feuillets,
  boucles).
- Une **évaluation de la qualité** : un coefficient de silhouette compris entre -1
  (mauvaise classification) et 1 (bonne classification), et un indice de Dunn d'autant
  plus grand que les clusters sont compacts et bien séparés. Ces mesures servent à
  comparer les algorithmes et à choisir le nombre de clusters.

## Utilisation

Exemple : de la lecture du PDB au clustering.

```python
import sys
sys.path.extend(["1.ATOM_AMINO", "2.PDB_STRUCT", "3.STATS"])

from PDBStructure import StructurePDB
from clustering import Kmeans

structure = StructurePDB("1tey_model1.pdb")
structure.compute_dihedrals()                 # remplit la liste des Point (phi, psi)
structure.write_dihedrals("angles.txt")       # écrit les angles dans un fichier

modele = Kmeans(structure._phipsi, 3)         # 3 groupes
modele.run()
print(modele.liste_k)                         # {numéro de cluster: liste de Point}
```

## Lancer les tests

Les tests importent les modules des autres dossiers : il faut déclarer ces dossiers
dans le chemin de Python.

Sous PowerShell, depuis la racine du dépôt :

```powershell
$env:PYTHONPATH = "1.ATOM_AMINO;2.PDB_STRUCT;3.STATS"
cd 4.TEST
python test_point.py
python test_Kmeans.py
```

Sous Linux ou macOS, remplacer les `;` du `PYTHONPATH` par des `:`.

`test_pdbstructure.py` lit `1tey_model1.pdb` avec un chemin relatif : il se lance depuis
la racine du dépôt (`python 4.TEST/test_pdbstructure.py`).
