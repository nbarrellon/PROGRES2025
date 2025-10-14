import sys
from socket import *


#On récupère les informations de connexion au serveur
arguments = sys.argv[1:]
serveurName = arguments[0]
serveurPort = int(arguments[1])
#----------------------------------------------------
#Le relai se comporte comme un serveur
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
serverSocket.bind(('127.0.0.1',5678)) 
serverSocket.listen(1) #ecoute sur le socket serveur
#----------------------------------------------
print("##############################################")
print("############## Relai démarré #################")
print("##############################################")
#------------------------------------------------
while True:
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    print("Connexion de ",address," Tunnel TCP ouvert")
    requete = connectionSocket.recv(2048)
    print("MESSAGE RECU DU CLIENT :",requete.decode('utf-8'))
    #Le relai se comporte maintenant comme un client
    clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
    
    try:
        clientSocket.connect((serveurName,serveurPort)) #il se connecte au serveur
        clientSocket.send(requete)
        reponse = clientSocket.recv(2048)
        print("Message reçu du serveur: ",reponse.decode('utf-8'))
    except ConnectionRefusedError:
        print("Impossible de se connecter au serveur.")
        reponse = "Le serveur est HS !".encode('utf-8')
    finally:
        print("Fermeture du tunnel TCP")
        clientSocket.close()
    
    #Le relai "redevient" serveur et transmets la réponse qu'il a reçue au client
    connectionSocket.send(reponse) 
    connectionSocket.close()

