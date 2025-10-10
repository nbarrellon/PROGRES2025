#Nils BARRELLON 21401602
#SERVEUR TCP QUI RENVOIE L'HEURE

from socket import *
from datetime import datetime
from time import time 
from struct import *

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
serverSocket.bind(('0.0.0.0',serverPort)) #permet d'écouter sur ttes les interfaces réseau disponibles
serverSocket.listen(1) #ecoute sur le socket serveur
print('Server ready. Want time ?')
while True:
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    requete = unpack("!d",connectionSocket.recv(2048))
    print("MESSAGE RECU",requete[0])
    tps_serveur = time()
    connectionSocket.send(pack("!d",tps_serveur)) #renvoie le temps horloge serveur
    print("Je renvoie au client le temps de mon horloge :",tps_serveur)
    connectionSocket.close()