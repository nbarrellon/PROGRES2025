#Nils BARRELLON 21401602
#CLIENT QUI PASSE PAR UN RELAI POUR ATTEINDRE LE SERVEUR

from socket import *

#-------------------------------------------------------------
# Informations de connexion au relai
serverName = '127.0.0.1'
serverPort = 5678

#-------------------------------------------------------------------
clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
try:
    clientSocket.connect((serverName,serverPort))
    message = input("Entrez le message à transmettre au serveur via le relai =>")
    clientSocket.send(message.encode('utf-8'))
    reponse = clientSocket.recv(2048).decode('utf-8')
    print("Message reçu du relai : ",reponse)
except ConnectionRefusedError:
    print("Impossible de se connecter au relai.")
finally:
    print("Fermeture du tunnel TCP")
    clientSocket.close()
           
