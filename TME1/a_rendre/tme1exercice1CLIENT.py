#Nils BARRELLON 21401602
# #CLIENT UDP

from socket import *
from random import randint
from time import perf_counter

def message_aleatoire(n:int)->str:
    """
    Entrée : n nbre de lettres du message à générer
    Sortie : une chaine de n caractères en minuscule
    """
    ch = ""
    for _ in range(n):
        ch += chr(randint(98,122))
    return ch

serverName = '127.0.0.1'
serverPort = 1234
temps = []
for i in range(10):
    clientSocket = socket(AF_INET,SOCK_DGRAM) #AF_INET : protocole IP, SOCK_DGRAM : UDP
    message = message_aleatoire(12)
    print("MESSAGE n°"+str(i)+":"+message)
    t0 = perf_counter()
    clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort)) #envoi d'un datagramme
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048) #reception de la réponse
    t1 = perf_counter()
    RTT = t1 - t0
    temps.append(RTT)
    print("MESSAGE RECU en :"+str(RTT)+" s ->" +modifiedMessage.decode('utf-8')+"\n")
    clientSocket.close()

print("RTT moyen = ",sum(temps)/len(temps),"s")