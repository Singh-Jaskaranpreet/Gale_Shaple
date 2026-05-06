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

L'algorithme de Gale-Shapley garantit une affectation stable, où aucune "paire instable" n'existe.

### Implémentations (Q3-Q5)

GS_Etudiant : Les étudiants proposent. Le résultat est optimal pour les étudiants.

GS_Parcours : Les masters proposent. Le résultat est optimal pour les parcours.

Pour GS_Etudiant :

1. **Trouver un étudiant libre**  
   Utilisation d'une pile (`self.libres`). On récupère un indice en $O(1)$ avec `.pop()`.

2. **Trouver le prochain parcours**  
   Chaque étudiant possède un compteur `self.proposition[i]` qui pointe vers l'index de son prochain vœu dans sa liste de préférences.

3. **Position de l'étudiant dans le classement du parcours**  
   Pour éviter une recherche en $O(n)$ à chaque fois, nous pré-calculons une matrice `rank_spe[parcours][etudiant]`.  
   Cela permet un accès en $O(1)$.

4. **Trouver l'étudiant le moins préféré**  
   Dans `self.cap_actu[j]`, nous maintenons la liste des admis triée $O(Capacite \log(Capacite))$.  
   Le moins préféré est donc toujours le dernier élément (`[-1]`) en $O(1)$.

5. **Remplacer un étudiant**  
   Lorsqu'un meilleur étudiant est accepté, on remplace le dernier par le nouveau, puis on re-trie (ou on insère de façon ordonnée) la liste.


Pour GS_Parcours :

1. **Trouver un parcours libre**  
   Utilisation d'un set (`self.libres`).  
   Un parcours est libre s'il a encore des places (`len(self.cap_actu[j]) < cap_max`) et des étudiants à contacter.  
   On récupère un indice en $O(1)$ avec `.pop()`.

2. **Trouver le prochain étudiant à solliciter**  
   Chaque parcours possède un compteur `self.proposition[j]` qui pointe vers le prochain étudiant dans sa liste de préférences `self.spe[j]`.

3. **Position du parcours dans le classement de l'étudiant**  
   Pour éviter une recherche en $O(n)$, nous pré-calculons une matrice `rank_etu[etudiant][parcours]`.  
   Cela permet à un étudiant de comparer deux parcours en $O(1)$.

4. **Décision de l'étudiant (le receveur)**  
   L'étudiant ne peut être affecté qu'à un seul parcours :
   - s'il est libre, il accepte,
   - sinon, il compare son parcours actuel avec le nouveau et garde le meilleur.

5. **Remplacer un étudiant**  
   Si un étudiant accepte un nouveau parcours :
   - il quitte son ancien parcours, qui redevient libre (ajouté à `self.libres`),
   - il est ajouté au nouveau parcours (`self.cap_actu[j]`),
   - `self.mariage[i]` est mis à jour.


### Complexité temporelle : $O(n \times m)$

- Le nombre total d'itérations est strictement borné par le produit du nombre d'étudiants ($n$) et du nombre de parcours ($m$).
- **Pire cas :** chaque parcours propose successivement ses places à tous les étudiants de sa liste.
- **Coût d'une itération :** grâce à la matrice `rank_etu`, chaque proposition est traitée en $O(1)$.

**Total :** $O(n \times m)$.

---

### Complexité spatiale : $O(n \times m)$

Le stockage de la matrice des rangs inversée occupe un espace proportionnel au produit des deux populations.

### Vérification de la Stabilité (Q6)

La fonction paires_instables analyse les mariages. Un couple $(e, s)$ est instable si :

L'étudiant $e$ préfère le master $s$ à son affectation actuelle.

Le master $s$ préfère l'étudiant $e$ à l'un de ses admis actuels.
Résultat : Gale-Shapley produit toujours 0 paire instable.

### Analyse de Performance (Q7-Q10)

Sur des données générées aléatoirement ($n=200$ à $2000$) :

Le nombre d'itérations suit une courbe en $O(n \times m)$.

Le temps d'exécution confirme l'efficacité de l'algorithme pour des instances de taille réelle.

## 4. Optimisation Linéaire avec Gurobi (Q11-Q15)

### Modélisation (Q11)

Le problème est modélisé avec des variables binaires $x_{i,j} \in \{0, 1\}$ avec $i$ les étudiants et $j$ les parcours.

Contrainte d'unicité : $$\forall i \in \{0, \dots, n-1\}, \quad \sum_{j=0}^{m-1} x_{i,j} = 1$$

Contrainte de capacité : $$\forall j \in \{0, \dots, m-1\}, \quad \sum_{i=0}^{n-1} x_{i,j} \leq C_j$$

### Maximisation de l'Utilité Totale (Q12)

Nous maximisons la somme des scores de Borda des étudiants et des parcours :


$$\text{Maximiser } Z = \sum_{i=0}^{n-1} \sum_{j=0}^{m-1} x_{i,j} \cdot (u_{i,j} + v_{j,i})$$

Observation : L'utilité totale est supérieure à celle de Gale-Shapley, mais la solution est instable (apparition de paires bloquantes). Le système privilégie le "bonheur global" au détriment de certains individus.

### Équité et Contrainte $k$ (Q13-Q14)

Pour éviter qu'un étudiant ne reçoive son dernier vœu (utilité 0), nous imposons :


$$\forall i, \sum_{j=0}^{m-1} x_{i,j} \cdot u_{i,j} \geq (m - k)$$

Test $k=5$ : L'utilité minimale passe de 0 à 5.

Analyse : Plus $k$ est petit, plus le problème est difficile. Si $k$ est trop petit, le modèle devient infaisable.

## 5. Synthèse et Comparaison Finale (Q15)

| Critère | Gale-Shapley | Q11 Max Utilité Min | Q12 Max Somme Utilités | Q14 Min k pour faisabilité |
|----------|----------------------|--------------------------|----------------------|----------------------|
| Utilité Moyenne Étudiants | 7,85 | 8,15 | 7,23 | 8,08 |
| Utilité Moyenne Parcours | 10,10 | 8,20 | 11,90 | 9,60 |
| Utilité Minimale Étudiants | 4,00 | 5,00 | 0,00 | 5,00 |
| Nombre de Paires Instables | 0 | 6 | 6 | 3 |