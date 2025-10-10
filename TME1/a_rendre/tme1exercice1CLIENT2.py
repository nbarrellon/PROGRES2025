#Nils BARRELLON 21401602
#CLIENT UDP QUI GERE LES NON-REPONSES

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
    delay = 0.1
    clientSocket = socket(AF_INET,SOCK_DGRAM) #AF_INET : protocole IP, SOCK_DGRAM : UDP
    clientSocket.settimeout(delay)
    message = message_aleatoire(12)
    print("---------------------------------")
    print("MESSAGE n°"+str(i+1)+":"+message)
    t0 = perf_counter()
    clientSocket.sendto(message.encode('utf-8'),(serverName,serverPort)) #envoi d'un datagramme
    while True:
        try : #on essaie de recevoir la réponse du serveur
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048) #reception de la réponse
            t1 = perf_counter()
            RTT = t1 - t0
            temps.append(RTT)
            print("MESSAGE RECU en :"+str(RTT)+" s ->" +modifiedMessage.decode('utf-8'))
            
            clientSocket.close()  # On ferme le socket après avoir reçu la réponse
            break  # On sort de la boucle while
        except timeout: #si une erreur timeout est levée on double le délai
            delay *= 2
            if delay > 1.0: #si le délai d'attente dépasse 1s, on abandonne.
                print("Le serveur ne répond pas ! Abandon !")
                
                clientSocket.close()  # On ferme le socket avant d'abandonner
                break  # On sort de la boucle while
            else:
                clientSocket.settimeout(delay) #on adapte le délai et on attend de nouveau la réponse du serveur
                continue
print("--------------------------------")
print("Sur 10 messages envoyés, j'ai reçu ",len(temps)," réponses") 
if temps: #si on a pu calculer au moins un RTT
    print("RTT moyen = ",sum(temps)/len(temps),"s")