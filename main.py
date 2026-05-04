from utils import * # Pour pouvoir utiliser les methodes de exemple.py
'''
print("bonjour")
maListe=exemple.lectureFichier("test.txt") # Execution de la methode lectureFichier du fichier exemple.
print(maListe)
print(len(maListe)) #Longueur de la liste.
exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier
'''
Etu=MatEtu("PrefEtu.txt") # Execution de la methode lectureFichier du fichier exemple.
print("Etudiant : \n", Etu)
Spe, Cap=MatSpe("PrefSpe.txt") # Execution de la methode lectureFichier du fichier exemple.
print("Parcours : \n", Spe)

print("Capacite : ",Cap)
gs_etudiant = GS_Etudiant(Etu, Spe, Cap)
gs_parcours = GS_Parcours(Etu, Spe, Cap)

gs_etudiant.gs_etu()
print("Mariage etu : ",gs_etudiant.get_mariage())

gs_parcours.gs_spe()
print("Mariage parcours :",gs_parcours.get_mariage())
print(gs_parcours.cap_actu)

print(f'Mariages instables : {paires_instables(gs_parcours.get_mariage(), Etu, Spe, Cap)}')

simu_perf()
simu_iterations()