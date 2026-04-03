def MatEtu(s): # Definition d'une fonction, avec un parametre (s). Ne pas oublier les ":"
    monFichier = open(s, "r") # Ouverture en lecture. Indentation par rapport a la ligne d'avant (<-> bloc).
    contenu = monFichier.readlines() # Contenu contient une liste de chainces de caracteres, chaque chaine correspond a une ligne       
    monFichier.close() #Fermeture du fichier
    contenu.remove(contenu[0])
    for i in range(len(contenu)) :
        contenu[i] = contenu[i].split()  
        contenu[i].remove(contenu[i][0])
        contenu[i].remove(contenu[i][0])
    
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
    for i in range(len(contenu)) :
        contenu[i] = contenu[i].split()  
        contenu[i].remove(contenu[i][0])
        contenu[i].remove(contenu[i][0])
    return contenu, capacite

class GS_Etudiant:

    def __init__(self, etu, spe, cap):
        self.etu = etu
        self.nb_etu = len(etu)
        self.spe = spe
        self.nb_spe = len(spe)
        self.cap_max = cap
        self.cap_actu = [[] for _ in range(self.nb_spe)]
        self.mariage = [-1] * self.nb_etu
        self.proposition = [[] for _ in range(self.nb_etu)]

    def trouve_etu(self):
        for i in range(self.nb_etu):
            if self.mariage[i] == -1:
                return i
        return -1

    def trouve_spe(self, etu_ind):
        propose = len(self.proposition[etu_ind])
        if propose < self.nb_spe :
            self.proposition[etu_ind].append(self.etu[etu_ind][propose])
            return self.etu[etu_ind][propose]
        return -1

    def pos_etu(self, etu_ind, spe_ind):
        return self.spe[spe_ind].index(etu_ind)

    def least_pref(self, spe_ind):
        pos_least = -1
        pos_etu = -1
        rep
        for etu in self.cap_actu[spe_ind] :
            pos_etu = self.pos_etu(etu, spe_ind)
            if pos_least < pos_etu :
                pos_least = pos_etu
                rep = etu
        return rep, pos_least

    def remplacer(self, etu1, etu2, spe_ind) :
        self.cap_actu[spe_ind].remove(etu1)
        self.cap_actu[spe_ind].append[etu2]
        self.mariage[etu1] = -1
        self.mariage[etu2] = spe_ind

    def gs_etu(self) :
        etu = self.trouve_etu()
        while etu != -1 :
            spe = self.trouve_spe(etu)
            if len(self.cap_actu[spe]) < self.cap_max[spe] :
                self.mariage[etu] = spe
                self.cap_actu[spe].append(etu)
            else :
                lp, lp_pos = self.least_pref(spe)
                if self.pos_etu(etu, spe) < lp_pos :
                    self.remplacer(lp, etu, spe)
            etu = self.trouve_etu()    

    def get_mariage(self) :
        return self.mariage

class GS_Parcours:

    def __init__(self, etu, spe, cap):
        self.etu = etu
        self.nb_etu = len(etu)
        self.spe = spe
        self.nb_spe = len(spe)
        self.cap_max = cap
        self.cap_actu = [[] for _ in range(self.nb_spe)]
        self.mariage = [-1] * self.nb_etu
        self.proposition = [[] for _ in range(self.nb_spe)]

    def trouve_etu(self, spe_ind):
        propose = len(self.proposition[spe])
        if propose < self.nb_etu :
            self.proposition[spe_ind].append(self.spe[spe_ind][propose])
            return self.spe[spe_ind][propose]
        return -1

    def trouve_spe(self):
        for i, p in enumerate(self.proposition) :
            if len(p) < self.cap_max[i] :
                return i

    def pos_spe(self, etu_ind, spe_ind):
        return self.etu[etu_ind].index(spe_ind)

    def least_pref(self, spe_ind):
        pos_least = -1
        pos_etu = -1
        for etu in self.cap_actu[spe_ind] :
            pos_etu = self.pos_etu(etu, spe_ind)
            if pos_least < pos_etu :
                pos_least = pos_etu
        return pos_least

    def remplacer(self, spe1, spe2, etu_ind) :
        self.cap_actu[spe1].remove(etu_ind)
        self.cap_actu[spe2].append[etu_ind]
        self.mariage[etu_ind] = spe2

    def gs_spe(self) :
        spe = self.trouve_spe()
        while spe != -1 :
            etu = self.trouve_etu(spe)
            if self.mariage[etu] == -1 :
                self.mariage[etu] = spe
                self.cap_actu[spe].append(etu)
            else :
                lp = self.mariage[etu]
                if self.pos_spe(etu) < self.pos_spe(lp) :
                    self.remplacer(lp, etu, spe)
            spe = self.trouve_spe()

    def get_mariage(self) :
        return self.mariage


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