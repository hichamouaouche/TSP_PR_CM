# TSP_PR_CM : Résolution du Problème du Voyageur de Commerce

## Description du Projet

**TSP_PR_CM** est un projet de recherche opérationnelle dédié à la comparaison et l'évaluation de plusieurs **métaheuristiques** pour résoudre le **Problème du Voyageur de Commerce (TSP)**. Le projet implémente cinq algorithmes de recherche et effectue une analyse comparative rigoureuse sur des instances de tailles différentes.

---

## Objectifs

- Implémenter et tester 5 métaheuristiques pour le TSP
- Comparer leurs performances (qualité, temps d'exécution, nombre d'évaluations)
- Générer des analyses statistiques et des visualisations graphiques
- Fournir une framework extensible pour ajouter de nouveaux algorithmes

---

## Métaheuristiques Implémentées

1. **Hill Climbing First** : Accepte le premier voisin qui améliore la solution
2. **Hill Climbing Best** : Explore tous les voisins et choisit le meilleur
3. **Multi-Start Hill Climbing** : Lance plusieurs Hill Climbing aléatories
4. **Simulated Annealing** : Recuit simulé avec refroidissement progressif
5. **Tabu Search** : Recherche tabou avec liste d'interdictions

---

## Structure du Projet

```
TSP_PR_CM/
├── algorithms.py           # Implémentations des 5 métaheuristiques
├── data_generator.py       # Génération des instances TSP
├── experiment.py           # Framework d'expérimentation et visualisations
├── README.md               # Cette documentation
│
├── data/                   # Instances TSP (JSON)
│   ├── instance_20.json
│   ├── instance_50.json
│   └── instance_80.json
│
├── results/                # Résultats des expériences (JSON)
│   ├── results_n20.json
│   ├── results_n50.json
│   └── results_n80.json
│
└── figures/                # Graphiques générés (PNG)
```

---

## Utilisation

### Prérequis
```bash
Python 3.7+
numpy
matplotlib
```

### Installation
```bash
pip install numpy matplotlib
```

### Exécution complète
```bash
python experiment.py
```

Cela va :
- Générer automatiquement les 3 instances TSP (20, 50, 80 villes)
- Exécuter les 5 algorithmes 30 fois sur chaque instance
- Générer des graphiques de comparaison
- Calculer et sauvegarder les statistiques

### Utilisation personnalisée
```python
from experiment import TSPExperiment

exp = TSPExperiment('data/instance_20.json')
results = exp.run_algorithm("Hill Climbing Best", num_runs=30)
exp.generate_comparison_table()
exp.plot_results()
exp.save_results()
```

---

## Résultats Attendus

Le projet génère :
- **Tableaux comparatifs** : Performances de chaque algorithme
- **Graphiques statistiques** :
  - Comparaison des coûts moyens
  - Distribution des coûts (boxplot)
  - Comparaison des temps d'exécution
  - Visualisation des meilleurs tours trouvés

---

## Analyse

Les résultats permettent d'analyser :
- **Qualité de solution** : Coût moyen et stabilité (écart-type)
- **Rapidité** : Temps moyen d'exécution
- **Efficacité** : Nombre moyen d'évaluations (effort de recherche)
- **Fiabilité** : Meilleure solution trouvée sur 30 exécutions

### Observations typiques
- **Hill Climbing First** : Très rapide mais moins bon en qualité
- **Hill Climbing Best** : Meilleur compromis qualité/temps
- **Multi-Start HC** : Excellente qualité, temps plus long
- **Simulated Annealing** : Bonne qualité, très consommateur en évaluations
- **Tabu Search** : Excellente qualité et efficacité

---

## Fichiers Principaux

### algorithms.py
Implémente la classe `TSPSolver` (base) et 5 variantes avec méthode `solve()` retournant (tour optimal, coût, historique).

### data_generator.py
Génère des instances TSP aléatoires avec coordonnées 2D et calcule les distances euclidiennes. Sauvegarde en JSON.

### experiment.py
Orchestre les expériences, calcule les statistiques, génère les graphiques et les tableaux de comparaison.

---

## Points Clés

✓ **Framework flexible** : Facile d'ajouter de nouveaux algorithmes  
✓ **Analyse statistique rigoureuse** : 30 exécutions par algorithme par instance  
✓ **Visualisations complètes** : 4 graphiques par instance  
✓ **Résultats reproductibles** : Graines fixes pour la génération des données  
✓ **Code bien structuré** : Classes orientées objet, commentaires détaillés  

---

## Conclusion

Ce projet fournit une plateforme complète pour étudier et comparer les métaheuristiques appliquées au TSP. Il démontre comment différentes approches de recherche influencent la qualité de la solution et le temps d'exécution.

