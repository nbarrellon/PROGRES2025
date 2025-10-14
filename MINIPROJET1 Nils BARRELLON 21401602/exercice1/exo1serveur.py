#Nils BARRELLON 21401602
#SERVEUR TCP QUI MET EN MAJUSCULE LA REQUETE DU CLIENT

from socket import *

#----------------------------------------------
serverPort = 1234 #en lieu et place du port habituel 80
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
serverSocket.bind(('0.0.0.0',serverPort)) #permet d'écouter sur ttes les interfaces réseau disponibles
serverSocket.listen(1) #ecoute sur le socket serveur
#----------------------------------------------
print("##############################################")
print("############## Serveur démarré ###############")
print("##############################################")

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
    print("Serveur en écoute sur l'adresse IP", get_local_ip())
    print("Port d'écoute :",serverPort)
    print("##############################################")
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    print("Connexion de ",address," Tunnel TCP ouvert")
    requete = connectionSocket.recv(2048).decode('utf-8')
    print("MESSAGE RECU",requete)
    requete = requete.upper()
    connectionSocket.send(requete.encode('utf-8')) 
    connectionSocket.close()

