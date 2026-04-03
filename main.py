import utils as u # Pour pouvoir utiliser les methodes de exemple.py
'''
print("bonjour")
maListe=exemple.lectureFichier("test.txt") # Execution de la methode lectureFichier du fichier exemple.
print(maListe)
print(len(maListe)) #Longueur de la liste.
exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier
'''
Etu=u.MatEtu("PrefEtu.txt") # Execution de la methode lectureFichier du fichier exemple.
print(Etu)
Spe, Cap=u.MatSpe("PrefSpe.txt") # Execution de la methode lectureFichier du fichier exemple.
print(Spe)

print(Cap)
gs_etudiant = u.GS_Etudiant(Etu, Spe, Cap)
gs_parcours = u.GS_Parcours(Etu, Spe, Cap)

gs_etudiant.gs_etu()
print(gs_etudiant.get_mariage())