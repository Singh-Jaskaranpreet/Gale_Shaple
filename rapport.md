# Rapport TME : Problèmes d'Affectation et Appariements

    • SINGH Jaskaranpreet 21239295
    • QU Guillaume 21316059

## 1. Introduction

Ce TME porte sur le problème de l'affectation stable, appliqué à la répartition d'étudiants dans des parcours de Master à la Sorbonne. Nous avons exploré deux approches fondamentales :

L'algorithme de Gale-Shapley (orienté stabilité).

La programmation linéaire avec Gurobi (orientée efficacité et équité).

## 2. Chargement des Données et Modélisation (Q1-Q3)

Les premières étapes consistent à transformer les données textuelles en structures informatiques exploitables.

Lecture des fichiers (Q1-Q2) : Les fonctions MatEtu et MatSpe nettoient les fichiers .txt pour extraire les préférences sous forme de listes d'entiers et récupérer les capacités d'accueil des parcours.


## 3. Algorithme de Gale-Shapley (Q4-Q10)

L'algorithme de Gale-Shapley garantit une affectation stable, où aucune "paire instable" (regret mutuel) n'existe.

### Implémentations (Q3-Q5)

GS_Etudiant : Les étudiants proposent. Le résultat est optimal pour les étudiants.

GS_Parcours : Les masters proposent. Le résultat est optimal pour les parcours.

Optimisation : Pour améliorer la performance, nous maintenons la liste des admis de chaque parcours triée par préférence. Cela permet d'identifier le "moins préféré" (le candidat à expulser) en temps constant $O(1)$.

### Vérification de la Stabilité (Q6)

La fonction paires_instables analyse les mariages. Un couple $(e, s)$ est instable si :

L'étudiant $e$ préfère le master $s$ à son affectation actuelle.

Le master $s$ préfère l'étudiant $e$ à l'un de ses admis actuels (ou a une place vide).
Résultat : Gale-Shapley produit toujours 0 paire instable.

### Analyse de Performance (Q7-Q10)

Sur des données générées aléatoirement ($n=200$ à $2000$) :

Le nombre d'itérations suit une courbe en $O(n \times m)$.

Le temps d'exécution confirme l'efficacité de l'algorithme pour des instances de taille réelle.

## 4. Optimisation Linéaire avec Gurobi (Q11-Q15)

### Modélisation (Q11)

Le problème est modélisé avec des variables binaires $x_{i,j} \in \{0, 1\}$.

Contrainte d'unicité : $\sum_{j=1}^{m} x_{i,j} = 1$ (chaque étudiant a un master).

Contrainte de capacité : $\sum_{i=1}^{n} x_{i,j} \leq C_j$ (respect des places disponibles).

### Maximisation de l'Utilité Totale (Q12)

Nous maximisons la somme des scores de Borda des étudiants et des parcours :


$$\text{Maximiser } Z = \sum_{i=1}^{n} \sum_{j=1}^{m} x_{i,j} \cdot (u_{i,j} + v_{j,i})$$

Observation : L'utilité totale est supérieure à celle de Gale-Shapley, mais la solution est instable (apparition de paires bloquantes). Le système privilégie le "bonheur global" au détriment de certains individus.

### Équité et Contrainte $k$ (Q13-Q14)

Pour éviter qu'un étudiant ne reçoive son dernier vœu (utilité 0), nous imposons :


$$\forall i, \sum_{j=1}^{m} x_{i,j} \cdot u_{i,j} \geq (m - k)$$

Test $k=5$ : L'utilité minimale passe de 0 à 5.

Analyse : Plus $k$ est petit, plus le problème est difficile. Si $k$ est trop petit, le modèle devient infaisable (Infeasible).

## 5. Synthèse et Comparaison Finale (Q15)

| Critère            | Gale-Shapley                 | Gurobi (Q12)                     | Gurobi (Q14)                      |
|--------------------|-----------------------------|----------------------------------|----------------------------------|
| Stabilité          | Parfaite (0 paire)          | Instable (ex: 6 paires)          | Instable (ex: 3 paires)          |
| Efficacité Globale | Moyenne                     | Maximale (Optimum social)        | Bonne                            |
| Satisfaction Min   | Faible (risque de vœu 10)   | Très faible (vœu 10 possible)    | Garantie (vœu k minimum)         |

## Conclusion

Ce TME met en lumière l'arbitrage fondamental entre stabilité et efficacité :

Gale-Shapley garantit la paix sociale (pas de contestation) mais peut être sous-optimal globalement.

L'optimisation linéaire permet de maximiser le bien-être collectif ou d'imposer des règles d'équité strictes, mais elle génère des frustrations locales (instabilités).

Dans un contexte réel, la solution de la Q14 semble la plus équilibrée, car elle permet de garantir à chaque étudiant un choix "raisonnable" tout en cherchant à satisfaire le plus grand nombre.