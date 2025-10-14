import sys
from socket import *
from struct import *
from recvallTCP import *
from datetime import datetime
from stats import *

#On récupère les informations de connexion au serveur fournis en ligne de commande
arguments = sys.argv[1:]
serveurName = arguments[0]
serveurPort = int(arguments[1])
#----------------------------------------------------
#Le relai se comporte comme un serveur
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
serverSocket.bind(('127.0.0.1',5678)) 
serverSocket.listen(1) #ecoute sur le socket serveur
#----------------------------------------------
print("##############################################")
print("############## Relai démarré #################")
print("##############################################")
#------------------------------------------------
dico_log = {}
while True:
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    print("Connexion de ",address," Tunnel TCP ouvert")
    try:
        requete = connectionSocket.recv(2048).decode('utf-8') #on garde recv car la requete est courte
        print("MESSAGE RECU DU CLIENT :",requete)
        commande = requete.split(" ")
        #print(commande)
        uri = commande[1] #on récupère le nom du fichier demandé
        serveurOK = False
        if len(commande)==3: #si l'utilisateur veut les stats...
            reponse = statistiques(dico_log,uri) #la réponse du relai est un message contenant les stats
        else:
            #Le relai se comporte maintenant comme un client et interroge le serveur
            clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
            try:
                clientSocket.connect((serveurName,serveurPort)) #il se connecte au serveur
                demande_get = "GET "+uri
                clientSocket.send(demande_get.encode('utf-8'))
                reponse = get_block(clientSocket) #on récupère le message
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
                #on cree l'entrée dans le dictionnaire log si on a obtenu une réponse du serveur
                if serveurOK:
                    # on récupère la date et l'heure actuelles
                    maintenant = datetime.now() 
                    # on la formater en chaîne de caractères
                    date_heure_chaine = maintenant.strftime("%d/%m/%Y %H:%M:%S")
                    #si cette URI a déjà été rencontrée, on met à jour les données la concernant
                    if uri in dico_log:
                        dico_log[uri]['ip'].append(address[0])
                        dico_log[uri]['date'].append(date_heure_chaine)
                        dico_log[uri]['reponse'].append(reponse.decode('utf-8'))
                    #sinon on crée l'entrée
                    else:
                        dico_log[uri] = {'ip':[address[0]],'date':[date_heure_chaine],'reponse':[reponse.decode('utf-8')]}
                    #print("LOG =>",dico_log)
            
        #Le relai "redevient" serveur et transmets la réponse qu'il a reçue au client
        put_block(connectionSocket,reponse) # car le fichier peut-être grand
    except Exception as e:
        print(f"Erreur avec le client : {e}")
    finally:
        connectionSocket.close()


