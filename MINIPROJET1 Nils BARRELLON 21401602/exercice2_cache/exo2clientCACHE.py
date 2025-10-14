#Nils BARRELLON 21401602
#CLIENT QUI PASSE PAR UN RELAI POUR ATTEINDRE LE SERVEUR

from socket import *
from recvallTCP import *

#-------------------------------------------------------------
# Informations de connexion au relai
serverName = '127.0.0.1'
serverPort = 5678

#-------------------------------------------------------------------
clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
try:
    clientSocket.connect((serverName,serverPort))
    #----------------------------------------------
    fichier = input("Quel fichier voulez-vous ? =>")
    requete = "GET " + fichier
    requete = requete.encode('utf-8')
    clientSocket.send(requete)
    try:
        # Lire la réponse HTTP ligne par ligne pour récupérer l'en-tête (de longueur variable selon la réponse)
        reponse = b""
        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            reponse += data
            # On s'arrête si on a lu la fin des en-têtes (ligne vide)
            #il est possible qu'on ait récupéré un peu du corps du message
            if b"\r\n\r\n" in reponse:
                break
        # On sépare les en-têtes du corps
        # Ignorer les 4 premiers octets (taille du message)
        if len(reponse) >= 4:
            reponse = reponse[4:]  # On saute les 4 premiers octets
        en_tete, corps = reponse.decode('utf-8').split("\r\n\r\n", 1)
        # Analyser les différents champs de l'en-tête
        headers = en_tete.split("\r\n")
        status = headers[0]
        print("Réponse HTTP : ",status)
        # Extraire la taille du contenu
        longueur = 0
        for header in headers[1:]:
            if header.lower().startswith("content-length:"):
                longueur = int(header.split(":")[1].strip()) 
        print("Taille en octets :",longueur)
        # Lire le reste du corps si nécessaire
        if longueur > 0:
            # Calculer la taille du corps déjà reçu
            restant = longueur - len(corps)
            # Lire le reste du corps
            if restant > 0:
                corps += recvall(clientSocket, restant)
            #ecrire le corps dans un nouveau fichier qui porte le même nom que celui demandé + "_copy"
            nom_fichier,extension = tuple(fichier.split('.'))
            fichier_copy = nom_fichier+"_copy."+extension
            print("Sauvegarde sous le nom :",fichier_copy)
            with open(fichier_copy,"w") as f:
                f.write(corps)
        else:
            print("Aucun contenu reçu.")
    except Exception as e:
        print(f"Erreur : {e}")
except ConnectionRefusedError:
    print("Impossible de se connecter au relai.")
except ConnectionResetError:
    print("La connexion a été fermée par le serveur.")
except socket.timeout:
    print("Timeout : Le serveur ne répond pas.")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    print("Fermeture du tunnel TCP")
    clientSocket.close()
           
