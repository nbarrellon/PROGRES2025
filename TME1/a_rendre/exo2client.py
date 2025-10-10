#Nils BARRELLON 21401602

from socket import *
from time import time
from struct import *

serverName = '127.0.0.1'
serverPort = 1234

difference = []

for i in range(10):
    clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
    clientSocket.connect((serverName,serverPort))
    print("--------------")
    print("CALCUL n°",i+1)
    t0 = time()
    print("Mon horloge quand j'envoie le message :",t0)
    temps_client = pack("!d",t0) #convertit le temps pour une conversation internet
    clientSocket.send(temps_client)
    t1 = unpack("!d",clientSocket.recv(2048))[0]
    print("Horloge côté serveur quand il a reçu mon message=",t1)
    t2 = time()
    print("Mon horloge quand je reçois son message=",t2)
    difference.append(abs((t1-t0)-(t2-t0)))
    clientSocket.close()
           
print("--------------------------------------")                
  
print("Différence d'horloge moyenne observée :",round(sum(difference)/len(difference),5))