from pathlib import Path


d = Path(".")
requete = input("Quel fichier voulez-vous ?")
for file in d.rglob('*'):
    print(file.name)
        
    if file.name == requete and file.is_file():
        chemin = file.as_posix()
        print("FICHIER EXISTANT ICI : ",chemin)
    else:
        reponse = "Erreur 404"
        print(reponse)