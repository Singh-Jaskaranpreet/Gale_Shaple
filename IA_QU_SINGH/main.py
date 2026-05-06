from utils import *

Etu=MatEtu("PrefEtu.txt")
print("Etudiant : \n", Etu)
Spe, Cap=MatSpe("PrefSpe.txt")
print("Parcours : \n", Spe)

print("Capacite : ",Cap)
gs_etudiant = GS_Etudiant(Etu, Spe, Cap)
gs_parcours = GS_Parcours(Etu, Spe, Cap)

gs_etudiant.gs_etu()
print("Mariage etu : ",gs_etudiant.get_mariage())

gs_parcours.gs_spe()
print("Mariage parcours :",gs_parcours.get_mariage())

print(f'Mariages instables : {paires_instables(gs_parcours.get_mariage(), Etu, Spe, Cap)}')

simu_perf()

aff_min, m_e_min, m_s_min, u_min =  resoudre_affectation_max_min(Etu, Spe, Cap)

aff_max, m_e_max, m_s_max, u_min_max = resoudre_affectation(Etu, Spe, Cap)

aff_k, m_e_k, m_s_k, k_min = question_14(Etu, Spe, Cap)

print("\n\nResoudre Affectation Q11")
print(f"Utilité moy Etu : {m_e_min}\nUtilité moy Spe : {m_s_min}\n Utilité min : {u_min}\n Affectation : {aff_min}")
print(f'Mariages instables : {paires_instables(aff_min, Etu, Spe, Cap)}')

print("\n\nResoudre Affectation Q12")
print(f"Utilité moy Etu : {m_e_max}\nUtilité moy Spe : {m_s_max}\n Utilité min : {u_min_max}\n Affectation : {aff_max}")
print(f'Mariages instables : {paires_instables(aff_max, Etu, Spe, Cap)}')

print("\n\nResoudre Affectation Q14")
print(f"Utilité moy Etu : {m_e_k}\nUtilité moy Spe : {m_s_k}\n K min : {u_min}\n Affectation : {aff_k}")
print(f'Mariages instables : {paires_instables(aff_k, Etu, Spe, Cap)}')
