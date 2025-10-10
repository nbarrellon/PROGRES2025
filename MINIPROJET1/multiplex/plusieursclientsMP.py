#Nils BARRELLON 21401602
#CLIENTS QUI EMPRUNTENT LE TUNNEL DE RELAI

from socket import *
from threading import *

#-------------------------------------------------------------
# Informations de connexion au relai
serverName = '127.0.0.1'
serverPort = 8080

def client(fichier,client):
    print("------------Client n°",client,"------------")
    print("Je demande l'URI :",fichier)
    print("-------------------------------------------")
    clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
    try:
        clientSocket.connect((serverName,serverPort))
        #----------------------------------------------
        requete = "GET " + fichier
        requete = requete.encode('utf-8')
        clientSocket.send(requete)
        try:
            reponse = clientSocket.recv(2048).decode('utf-8')
            print("Message reçu du serveur MP : ",reponse)
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
#-------------------------------------------------------------------
# on cree autant de thread que de client
from random import randint
requete = ['film1.txt',"foo.txt","foo.txt STATS","cochon.txt","cochon.txt STATS","musique1.txt","musique1.txt STATS"]
for n_client in range(5):
    i = randint(0,len(requete)-1)
    Thread(target=client,args=(requete[i],n_client)).start()
    
           
