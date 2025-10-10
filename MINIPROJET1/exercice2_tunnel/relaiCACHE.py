import sys
from socket import *
from struct import *
from recvallTCP import *

port = 55553
#----------------------------------------------------
#Le relai se comporte comme un serveur
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
serverSocket.bind(('127.0.0.1',port))
serverSocket.listen(1) #ecoute sur le socket serveur
#----------------------------------------------
print("----------------------------------------------")
print(f"---- Relai CACHE démarré : port = {port} ----")
print("----------------------------------------------")
#------------------------------------------------
dico_uri = {}
while True:
    print("Je suis à l'écoute...")
    print("------------------------------------------")
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    print("Connexion de ",address," Tunnel TCP ouvert")
    try:
        requete = connectionSocket.recv(2048).decode('utf-8') #on garde recv car la requete est courte
        print("MESSAGE RECU DU CLIENT :",requete)
        uri = requete[4:]
        serveurOK = False
        #on vérifie si le fichier demandé ne l'a pas déjà été
        if uri in dico_uri:
            print("Cette URI a déjà été demandée, elle est en cache")
            reponse = dico_uri[uri] #on récupère la réponse à envoyer
        else:
            #Le relai se comporte maintenant comme un client
            clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
            try:
                #ce relai se connecte au serveur
                serveurName = "127.0.0.1"
                serveurPort = 8080
                clientSocket.connect((serveurName,serveurPort)) #il se connecte au serveur
                clientSocket.send(requete.encode('utf-8'))
                reponse = get_block(clientSocket) #on récupère le message
                #reponse = clientSocket.recvall(2048) 
                #print("Message reçu du serveur: ",reponse.decode('utf-8'))
                serveurOK = True
            except ConnectionRefusedError:
                print("Impossible de se connecter au serveur.")
                reponse = "Le serveur est HS !".encode('utf-8')
            except ConnectionResetError:
                print("Connexion interrompue par le serveur.")
                reponse = "Erreur : Connexion interrompue.".encode('utf-8')
            finally:
                print("Fermeture du tunnel TCP")
                clientSocket.close()
                #on cree l'entrée dans le dictionnaire cache si on a obtenu une réponse du serveur
                if serveurOK:
                    dico_uri[uri] = reponse
        
        #Le relai "redevient" serveur et transmets la réponse qu'il a reçue au client
        put_block(connectionSocket,reponse) # car le fichier peut-être grand
    except Exception as e:
        print(f"Erreur avec le client : {e}")
    finally:
        connectionSocket.close()


