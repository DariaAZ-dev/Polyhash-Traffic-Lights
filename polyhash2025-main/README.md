# Projet Poly# 2025

## Titre, nom et composition de l'équipe

**Nom du projet :** PolyHash Traffic Optimizer

**Membres de l'équipe :**
- KOUAM MEULAK - meulak.kouam@etu.univ-nantes.fr
- Liban Mohamed Ali - liban.mohamed-ali@etu.univ-nantes.fr
- Daria Zinich - [Email]

## Descriptif général du projet

Ce projet a été réalisé dans le cadre du module d'optimisation Poly#. L'objectif est de concevoir et d'implémenter un algorithme capable d'optimiser la planification des feux de signalisation dans une ville.

À partir d'une description du réseau routier (intersections, rues, durées de trajet) et des itinéraires de nombreux véhicules, le programme doit générer un plan de feux (quelle rue a le feu vert et pour combien de temps) afin de minimiser le temps d'attente total et maximiser le score global.

## Répartition des tâches

- **KOUAM MEULAK** : Implémentation du parseur (`polyparser.py`) et de l'heuristique principale (`polysolver_4.py`).
- **Liban Mohamed Ali** : Développement du moteur de scoring (`polyscorer.py`) et du script de benchmark via `test_all_challenges.py`.
- **Daria Zinich** : Recherche et implémentation des stratégies alternatives (Linear Ratio et interpolation dans `polysolver_3.py` et `polysolver_2.py`).

## Procédure d'installation

Le projet est développé en **Python 3**. Il ne nécessite aucune installation de dépendance externe complexe (librairies standard utilisées).

1. **Cloner le dépôt :**
   ```bash
   git clone https://gitlab.univ-nantes.fr/E25B834U/polyhash2025
   cd polyhash2025
   ```

2. **Pré-requis :** Avoir Python 3 installé sur la machine.

## Procédure d'exécution

Le point d'entrée du programme est le fichier `polyhash.py`.

**Syntaxe :**
```bash
python polyhash.py <fichier_entree.in> <fichier_sortie.txt>
```

**Exemple d'exécution :**
```bash
python polyhash.py challenges/b_ocean.in submission_b.txt
```

Le programme affichera la progression du chargement, le lancement du solveur, la sauvegarde du résultat, et enfin le score estimé de la solution.

## Détail des stratégies mises en oeuvre et performances

Nous avons itéré sur plusieurs heuristiques pour améliorer progressivement notre score. Toutes les stratégies sont conservées dans le code pour comparaison.

### 1. Heuristique Naïve (Round Robin) - `polysolver.py`
Il s'agit de notre stratégie de base (Baseline).
- **Principe** :
    - Si une intersection a 1 seule rue entrante : Feu vert permanent.
    - Si plusieurs rues entrantes : Cycle simple "Round Robin" où chaque rue active reçoit **1 seconde** de vert tour à tour.
- **Performance** : Cette méthode assure que personne n'est bloqué indéfiniment, mais est inefficace pour les rues à fort trafic qui nécessitent plus de temps.

### 2. Heuristique Linear Ratio - `polysolver_3.py`
Cette stratégie tente d'adapter la durée du feu vert à la demande.
- **Principe** :
    - On définit un "budget temps" pour l'intersection (`MAX_Ti`).
    - Le temps alloué à chaque rue est proportionnel à son trafic par rapport au trafic total du carrefour.
    - Formule : `Durée = (Trafic_Rue / Trafic_Total) * Budget`.
- **Performance** : Améliore le flux sur les grosses intersections, mais peut pénaliser les petites rues si le budget est mal calibré.

### 3. Heuristique Square Root Scaling - `polysolver_2.py`
Une variante de la précédente pour lisser les écarts.
- **Principe** :
    - Au lieu d'utiliser le trafic brut, on utilise la **racine carrée** du trafic (`sqrt(traffic)`).
    - Cela réduit l'écart entre les rues très chargées et les rues peu chargées, évitant la famine des petites rues.
    - Utilise une interpolation linéaire pour projeter ces scores sur une plage de temps [`min_time`, `max_time`].

### 4. Heuristique Bracket Scaling (Stratégie Finale) - `polysolver_4.py`
C'est la stratégie utilisée par défaut dans `polyhash.py` (polysolver_4) car elle offre les meilleurs résultats globaux.
- **Principe** :
    1. **Tri par Priorité** : Les rues sont priorisées en fonction des "Starters" (voitures présentes au temps T=0) puis du volume total. L'évacuation des voitures présentes au démarrage est critique pour éviter les bouchons précoces.
    2. **Système de Paliers (Brackets)** : Au lieu de calculs proportionnels continus, nous utilisons des paliers fixes pour assigner les durées de feu vert :
        - 1 à 10 voitures : **1s**
        - 11 à 50 voitures : **2s**
        - 51 à 200 voitures : **3s**
        - > 200 voitures : **4s**
- **Commentaire sur la performance** : Cette approche discrète est extrêmement rapide (complexité O(N)) car elle évite les opérations flottantes coûteuses. Elle s'est révélée la plus robuste sur l'ensemble des datasets (A à F).

## Description de l'organisation du code

Le code est organisé en modules fonctionnels :

- `polyhash.py` : **Main**. Orchestre tout le processus (Parsing -> Solving -> Saving -> Scoring).
- `polyparser.py` : Contient `parse_challenge()`. Lit les fichiers `.in` et structure les données.
- `polyscorer.py` : Contient `score_solution()`. Simule le trafic pour calculer le score localement.
- `solver_3.py` : **Meilleur Solveur**. Contient l'implémentation de la stratégie "Bracket Scaling".
- `solver_2.py` : Contient l'implémentation "Linear Ratio".
- `polysolver.py` : Contient l'implémentation de base "Round Robin".
- `polysolver_2.py` : Contient les expérimentations sur l'interpolation (Square Root).
- `test_all_challenges.py` : Script pour lancer et comparer les solveurs sur tous les fichiers d'un coup.

## Bugs et limitations connus

- **Dépendances Inter-Carrefours** : Notre heuristique traite chaque intersection indépendamment. Elle ne prend pas en compte les "vagues vertes" (coordination entre carrefours voisins).
- **Modèle Statique** : La décision est basée sur les données initiales du problème. L'algorithme ne s'adapte pas dynamiquement si le trafic évolue différemment de la prévision statistique (bien que le modèle du concours soit déterministe).
