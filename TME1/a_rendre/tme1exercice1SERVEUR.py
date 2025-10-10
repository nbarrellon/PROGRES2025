#Nils BARRELLON 21401602
from socket import *
serverPort = 1234
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print('server ready')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode('utf-8').upper()
    serverSocket.sendto(modifiedMessage.encode('utf-8'),clientAddress)
