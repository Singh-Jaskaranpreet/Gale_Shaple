import time
import random
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB

def MatEtu(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    contenu.remove(contenu[0])
    for i in range(len(contenu)) :
        contenu[i] = contenu[i].split()  
        contenu[i].remove(contenu[i][0])
        contenu[i].remove(contenu[i][0])
        contenu[i] = list(map(int, contenu[i]))
    return contenu


def MatSpe(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    contenu.remove(contenu[0])
    capacite = contenu[0]
    contenu.remove(capacite)
    capacite = capacite.split()
    capacite.remove(capacite[0])
    capacite = list(map(int, capacite))
    for i in range(len(contenu)) :
        contenu[i] = contenu[i].split()  
        contenu[i].remove(contenu[i][0])
        contenu[i].remove(contenu[i][0])
        contenu[i] = list(map(int, contenu[i]))
    return contenu, capacite

def createFichierLP(nomFichier,nombreVariables):
    monFichier=open(nomFichier,"w") #Ouverture en ecriture. Le fichier est ecrase s'il existe, cree s'il n'existe pas
    monFichier.write("Maximize\n")
    for i in range(0,nombreVariables): #Boucle i variant de 0 a NombreVariables-1
        monFichier.write("x"+str(i)+" ") #write pour ecrire. Indentation
        if (i<nombreVariables-1): # Syntaxe d'un test. 'and' et 'or' dans les expressions logique
            monFichier.write("+ ")
        else:
            monFichier.write("\n")
    monFichier.write("st\n") # Fin de l'indentation -> fin de la boucle
    monFichier.write("Binary\n")
    for i in range(0,nombreVariables):
        monFichier.write("x"+str(i)+" ")
    monFichier.write("\n")
    monFichier.write("end")
    monFichier.close()

class GS_Etudiant:

    def __init__(self, etu, spe, cap):
        self.etu = etu
        self.nb_etu = len(etu)
        self.spe = spe
        self.nb_spe = len(spe)
        self.cap_max = cap

        self.rank_spe = [[0] * self.nb_etu for _ in range(self.nb_spe)]
        for s in range(self.nb_spe):
            for rank, e in enumerate(self.spe[s]):
                self.rank_spe[s][e] = rank

        self.libres = list(range(self.nb_etu))
        self.cap_actu = [[] for _ in range(self.nb_spe)]
        self.mariage = [-1] * self.nb_etu
        self.proposition = [0] * self.nb_etu

        self.cpt = 0

    def trouve_etu(self):
        if self.libres:
            return self.libres.pop()
        return -1

    def trouve_spe(self, etu_ind):
        p = self.proposition[etu_ind]
        if p < self.nb_spe :
            self.proposition[etu_ind] += 1
            return self.etu[etu_ind][p]
        return -1

    def pos_etu(self, etu_ind, spe_ind):
        return self.rank_spe[spe_ind][etu_ind]

    def least_pref(self, spe_ind):
        pos_least = -1
        rep = None
        ind = -1
        for i in range(len(self.cap_actu[spe_ind])):
            etu = self.cap_actu[spe_ind][i]
            rang_actu = self.pos_etu(etu, spe_ind)
            if rang_actu > pos_least: 
                pos_least = rang_actu
                rep = etu
                ind = i
        return rep, pos_least, ind

    def remplacer(self, etu_anc, etu_nv, spe_ind, etu_anc_ind):

        self.cap_actu[spe_ind][etu_anc_ind] = etu_nv
        
        self.mariage[etu_anc] = -1
        self.mariage[etu_nv] = spe_ind
        
        self.libres.append(etu_anc)

    def gs_etu(self) :
        etu = self.trouve_etu()
        while etu != -1 :
            self.cpt += 1
            spe = self.trouve_spe(etu)

            if len(self.cap_actu[spe]) < self.cap_max[spe] :
                self.mariage[etu] = spe
                self.cap_actu[spe].append(etu)
            else :
                lp_etu, lp_pos, lp_ind = self.least_pref(spe)
                if self.pos_etu(etu, spe) < lp_pos :
                    self.remplacer(lp_etu, etu, spe, lp_ind)
                else :
                    self.libres.append(etu)
            etu = self.trouve_etu()   
        return self.mariage 

    def get_mariage(self) :
        return self.mariage

class GS_Parcours:

    def __init__(self, etu, spe, cap):
        self.etu = etu
        self.nb_etu = len(etu)
        self.spe = spe
        self.nb_spe = len(spe)
        self.cap_max = cap

        self.rank_etu = [[0] * self.nb_spe for _ in range(self.nb_etu)]
        for e in range(self.nb_etu):
            for rank, s in enumerate(self.etu[e]):
                self.rank_etu[e][s] = rank

        self.libres = list(range(self.nb_spe))
        self.cap_actu = [[] for _ in range(self.nb_spe)]
        self.mariage = [-1] * self.nb_etu
        self.proposition = [0] * self.nb_spe

        self.cpt = 0

    def trouve_etu(self, spe_ind):
        p = self.proposition[spe_ind]
        if p < self.nb_etu:
            self.proposition[spe_ind] += 1
            return self.spe[spe_ind][p]
        return -1

    def trouve_spe(self):
        if self.libres : 
            return self.libres.pop()
        return -1
            
    def pos_etu(self, etu_ind, spe_ind):
        return self.spe[spe_ind].index(etu_ind)

    def pos_spe(self, etu_ind, spe_ind):
        return self.rank_etu[etu_ind][spe_ind]

    def remplacer(self, spe_anc, spe_nv, etu_ind) :
        self.cap_actu[spe_anc].remove(etu_ind)
        self.cap_actu[spe_nv].append(etu_ind)
        self.mariage[etu_ind] = spe_nv

        if spe_anc not in self.libres:
            self.libres.append(spe_anc)

    def gs_spe(self) :
        spe = self.trouve_spe()
        while spe != -1 :
            self.cpt += 1
            etu = self.trouve_etu(spe)
            if self.mariage[etu] == -1:
                self.mariage[etu] = spe
                self.cap_actu[spe].append(etu)
            else:
                spe_actuel = self.mariage[etu]
                if self.pos_spe(etu, spe) < self.pos_spe(etu, spe_actuel):
                    self.remplacer(spe_actuel, spe, etu)

            if len(self.cap_actu[spe]) < self.cap_max[spe] and self.proposition[spe] < self.nb_etu:
                if spe not in self.libres:
                    self.libres.append(spe)
            spe = self.trouve_spe()
        return self.mariage

    def get_mariage(self) :
        return self.mariage


def paires_instables(mariage, pref_etu, pref_spe, cap_max):
    instables = []
    nb_etu = len(pref_etu)
    nb_spe = len(pref_spe)

    # Reconstruire qui est dans quel parcours
    admis_actuels = [[] for _ in range(nb_spe)]
    for e, s in enumerate(mariage):
        if s != -1:
            admis_actuels[s].append(e)

    for e in range(nb_etu):
        s_actuel = mariage[e]
        vœux_e = pref_etu[e]
        
        # Trouver l'index du master actuel dans les vœux de l'étudiant
        idx_limite = vœux_e.index(s_actuel) if s_actuel != -1 else len(vœux_e)
        
        # L'étudiant regarde tous les masters qu'il préfère à son actuel
        for s_mieux in vœux_e[:idx_limite]:
            # Le master s_mieux préfère-t-il 'e' à l'un de ses admis ?
            if len(admis_actuels[s_mieux]) < cap_max[s_mieux]:
                instables.append((e, s_mieux))
            else:
                # Le master est plein, on cherche s'il y a un "moins bien classé" que 'e'
                pref_s = pref_spe[s_mieux]
                rang_e = pref_s.index(e)
                for admis in admis_actuels[s_mieux]:
                    if rang_e < pref_s.index(admis):
                        if (e, s_mieux) not in instables:
                            instables.append((e, s_mieux))
                        break
    return instables

def generer_donnees(n):
    # Q7: Préférences aléatoires
    pref_etu = [random.sample(range(9), 9) for _ in range(n)]
    pref_spe = [random.sample(range(n), n) for _ in range(9)]
    
    # Q8: Capacités équilibrées (Somme = n)
    base_cap = n // 9
    reste = n % 9
    caps = [base_cap + (1 if i < reste else 0) for i in range(9)]
    
    return pref_etu, pref_spe, caps

def simu_perf():
    tailles = range(200, 2001, 200)
    temps_etu = []
    temps_spe = []

    for n in tailles:
        t_etu_acc = 0
        t_spe_acc = 0
        nb_tests = 10
        
        for _ in range(nb_tests):
            E, S, C = generer_donnees(n)
            
            # Mesure GS_Etudiant
            g_e = GS_Etudiant(E, S, C)
            start = time.time()
            g_e.gs_etu()
            t_etu_acc += (time.time() - start)
            
            # Mesure GS_Parcours
            g_s = GS_Parcours(E, S, C)
            start = time.time()
            g_s.gs_spe()
            t_spe_acc += (time.time() - start)
            
        temps_etu.append(t_etu_acc / nb_tests)
        temps_spe.append(t_spe_acc / nb_tests)

    # Affichage Q8
    plt.plot(tailles, temps_etu, label="GS_Etudiant")
    plt.plot(tailles, temps_spe, label="GS_Parcours")
    plt.xlabel("Nombre d'étudiants (n)")
    plt.ylabel("Temps moyen (secondes)")
    plt.legend()
    plt.show()

def simu_iterations():
    tailles = range(200, 2001, 200)
    it_etu = []
    it_spe = []

    for n in tailles:
        total_it_etu = 0
        total_it_spe = 0
        
        for _ in range(10):
            E, S, C = generer_donnees(n)
            
            g_e = GS_Etudiant(E, S, C)
            g_e.gs_etu()
            total_it_etu += g_e.cpt
            
            g_p = GS_Parcours(E, S, C)
            g_p.gs_spe()
            total_it_spe += g_p.cpt
            
        it_etu.append(total_it_etu / 10)
        it_spe.append(total_it_spe / 10)

    # Affichage
    plt.plot(tailles, it_etu, label="Itérations GS Étudiant")
    plt.plot(tailles, it_spe, label="Itérations GS Parcours")
    plt.xlabel("Nombre d'étudiants (n)")
    plt.ylabel("Nombre moyen d'itérations")
    plt.legend()
    plt.show()


def resoudre_affectation(pref_etu, pref_spe, capacites, k_limite=None):
    # n = 13 (étudiants), m = 10 (parcours)
    n = len(pref_etu)
    m = len(pref_spe)
    
    # 1. Création du modèle
    model = gp.Model("Affectation_Sorbonne")
    
    # 2. Variables de décision : x[i,j] = 1 si l'étudiant i va dans le parcours j
    x = model.addVars(n, m, vtype=GRB.BINARY, name="x")

    # 3. Calcul des utilités (Scores de Borda)
    # Utilité etu[i][j] : quel score l'étudiant i donne au parcours j
    u_etu = [[0]*m for _ in range(n)]
    for i in range(n):
        for rang, j in enumerate(pref_etu[i]):
            u_etu[i][j] = (m - 1) - rang
            
    # Utilité spe[j][i] : quel score le parcours j donne à l'étudiant i
    u_spe = [[0]*n for _ in range(m)]
    for j in range(m):
        for rang, i in enumerate(pref_spe[j]):
            u_spe[j][i] = (n - 1) - rang

    # 4. Contraintes
    # Chaque étudiant est affecté à EXACTEMENT un parcours
    model.addConstrs((x.sum(i, '*') == 1 for i in range(n)), name="Unicite")
    
    # Chaque parcours respecte sa capacité maximale
    model.addConstrs((x.sum('*', j) <= capacites[j] for j in range(m)), name="Capacite")

    # Question Q13/Q14 : Contrainte des k-premiers choix
    # Un étudiant i est dans ses k premiers choix si son utilité >= (m - k)
    if k_limite is not None:
        for i in range(n):
            model.addConstr(gp.quicksum(x[i, j] * u_etu[i][j] for j in range(m)) >= (m - k_limite))

    # 5. Fonction Objectif (Q12 : Maximiser la somme des utilités totales)
    obj = gp.quicksum(x[i, j] * (u_etu[i][j] + u_spe[j][i]) for i in range(n) for j in range(m))
    model.setObjective(obj, GRB.MAXIMIZE)

    # 6. Optimisation
    model.optimize()

    # 7. Récupération des résultats
    if model.status == GRB.OPTIMAL:
        affectation = [-1] * n
        for i in range(n):
            for j in range(m):
                if x[i, j].X > 0.5:
                    affectation[i] = j
        
        # Calcul des statistiques pour Q12 / Q15
        util_max = sum(u_etu[i][affectation[i]] for i in range(n))
        util_moy = util_max / n
        util_min_etu = min(u_etu[i][affectation[i]] for i in range(n))
        
        return affectation, util_max, util_moy, util_min_etu
    else:
        return None, None, None, None

def question_14(pref_etu, pref_spe, capacites):
    print("--- Recherche du plus petit k (Question 14) ---")
    
    # On teste k de 1 (1er choix uniquement) à 10 (tous les choix possibles)
    for k in range(1, 11):
        print(f"\nEssai pour k = {k}...")
        aff, maxi, moy, mini = resoudre_affectation(pref_etu, pref_spe, capacites, k_limite=k)
        
        if aff is not None:
            print(f"SUCCÈS : Mariage parfait trouvé pour k = {k} !")
            print(f"Affectation obtenue : {aff}")
            paires = paires_instables(aff, pref_etu, pref_spe, capacites)
            print(f"Nombre de paires instables : {len(paires)}")
            print(f"Utilité moyenne : {moy:.2f}")
            print(f"Utilité minimale : {mini}")
            return aff, maxi, moy, mini, k
        else:
            print(f"ÉCHEC : Pas de solution pour k = {k}")