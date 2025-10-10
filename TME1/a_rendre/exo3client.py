#Nils BARRELLON 21401602

from socket import *
from struct import *
#----------------------------------------------
def get_block(sock):
    data = recvall(sock, header_struct.size)
    (block_length,) = header_struct.unpack(data)
    return recvall(sock, block_length)
#----------------------------------------------
def recvall(sock, length): #pour recevoir l'entiereté du fichier
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left in this block'.format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)

header_struct = Struct('!I')
#----------------------------------------------
serverName = '127.0.0.1'
serverPort = 1234
#----------------------------------------------
clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
try: #si jamais le serveur n'est pas actif
    clientSocket.connect((serverName,serverPort))
    #----------------------------------------------
    requete = input("Quel fichier voulez-vous ? =>")
    requete = "GET " + requete
    requete = requete.encode('utf-8')
    clientSocket.send(requete)
    try:
        # Lire la réponse HTTP ligne par ligne pour récupérer l'en-tête (de longueur variable selon la réponse)
        reponse = b""
        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            reponse += data
            # On s'arrête si on a lu la fin des en-têtes (ligne vide)
            #il est possible qu'on ait récupéré un peu du corps du message
            if b"\r\n\r\n" in reponse:
                break
        reponse_str = reponse.decode('utf-8')
        # On sépare les en-têtes du corps
        en_tete, corps = reponse_str.split("\r\n\r\n", 1)
        # Analyser les en-têtes
        headers = en_tete.split("\r\n")
        status = headers[0]
        print("Réponse HTTP : ",status)
        # Extraire la taille du contenu
        longueur = 0
        for header in headers[1:]:
            if header.lower().startswith("content-length:"):
                longueur = int(header.split(":")[1].strip()) 
        print("Taille en octets :",longueur)
        # Lire le reste du corps si nécessaire
        if longueur > 0:
            # Calculer la taille du corps déjà reçu
            corps_recu = len(corps.encode('utf-8'))
            restant = longueur - corps_recu
            # Lire le reste du corps
            if restant > 0:
                corps += recvall(clientSocket, restant).decode('utf-8')
            print("Contenu reçu :")
            print(corps)
        else:
            print("Aucun contenu reçu.")
    except Exception as e:
        print(f"Erreur : {e}")
    #----------------------------------------------
except ConnectionRefusedError:
    print("Impossible de se connecter au serveur.")
print("Fermeture du tunnel TCP")
clientSocket.close()
           
