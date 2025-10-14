#Nils BARRELLON 21401602

#SERVEUR TCP QUI SIMULE UN SERVEUR WEB
#----------------------------------------------
from socket import *
from time import time 
from struct import *
from pathlib import Path
import os
from recvallTCP import *

#----------------------------------------------
serverPort = 1234 #en lieu et place du port habituel 80
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
serverSocket.bind(('0.0.0.0',serverPort)) #permet d'écouter sur ttes les interfaces réseau disponibles
serverSocket.listen(1) #ecoute sur le socket serveur
#----------------------------------------------
print("######### Serveur démarré ###############")
# Fonction pour obtenir l'adresse IP locale
def get_local_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # On se connecte à un serveur externe (non résolu) pour obtenir l'IP locale
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

#------------------------------------------------
while True:
    print("--------------------------")
    print("Serveur en écoute sur l'adresse IP", get_local_ip())
    print("Port d'écoute :",serverPort)
    print("--------------------------")
    envoi = False
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    print("Connexion de ",address," Tunnel TCP ouvert")
    requete = connectionSocket.recv(2048).decode('utf-8')
    fichier = requete[4:]
    print("REQUETE RECUE : ",requete)
    print("FICHIER DEMANDE :",fichier)
    d = Path('.') #recherche du fichier depuis le répertoire courant.
    #On envoie le premier fichier portant ce nom qui est trouvé
    repertoire_courant = os.getcwd()
    print("Répertoire courant du serveur :",repertoire_courant )
    for file in d.rglob('*'): 
        if file.name == fichier and file.is_file():
            chemin = file.as_posix()
            print("FICHIER EXISTANT ICI : ./"+chemin)
            print("Lecture du fichier")
            with open(chemin, 'rb') as f:
                txt = f.read() #txt est en byte
            block_length = len(txt)
            #formatage de la réponse. On considère que le fichier est un fichier txt
            reponse = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {block_length}\r\n\r\n"
                f"{txt.decode("utf-8")}"
            )
            
            print("-----------------------------")
            print(reponse)
            #on envoie la réponse
            put_block(connectionSocket,reponse.encode('utf-8'))
            envoi = True
            break
    if not envoi: #le fichier n'a pas été trouvé
        print("LE FICHIER DEMANDE N'EXISTE PAS ! J'envoie Erreur 404.")
        print("Fermeture du tunnel TCP")
        #formatage de la réponse HTTP
        erreur = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 9\r\n\r\n"
        "Not Found"
        )
        put_block(connectionSocket,erreur.encode('utf-8'))
        #connectionSocket.sendall(erreur.encode('utf-8'))
    connectionSocket.close()