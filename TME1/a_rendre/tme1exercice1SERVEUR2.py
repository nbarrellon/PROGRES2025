#Nils BARRELLON 21401602
#serveur qui oublie de répondre une fois sur deux
from socket import *
from random import random


serverPort = 1234
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('server ready')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print("-----------------------------------------------------------")
    print("MESSAGE RECU de ",clientAddress," : ",message.decode('utf-8'))
    if random()<0.5:
        print("---------------------------")
        print("J'ai choisi de répondre :-)")
        modifiedMessage = message.decode('utf-8').upper()
        print("J'envoie au client le message : ",modifiedMessage)
        serverSocket.sendto(modifiedMessage.encode('utf-8'),clientAddress)
        
    else:
        print("J'ai décidé d'ignorer ce message")
        