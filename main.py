from utils import * # Pour pouvoir utiliser les methodes de exemple.py

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

aff, maxi, moy, mini = resoudre_affectation(Etu, Spe, Cap)

aff2, maxi2, moy2, mini2, k_min = question_14(Etu, Spe, Cap)

print("Resoudre Affectation Q12")
print(f"Utilité maximale : {maxi}\nUtilité moyenne : {moy}\n Utilité min : {mini}\n Affectation : {aff}")
print(f'Mariages instables : {paires_instables(aff, Etu, Spe, Cap)}\n')
print("Resoudre Affectation Q14")
print(f"Utilité moyenne : {maxi2}\n Utilité min : {mini2}\n Affectation : {aff2}, K_min : {k_min}")
print(f'Mariages instables : {paires_instables(aff2, Etu, Spe, Cap)}')
