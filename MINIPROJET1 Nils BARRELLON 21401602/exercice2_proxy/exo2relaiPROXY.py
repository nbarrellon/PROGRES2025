import sys
from socket import *
from struct import *
from recvallTCP import *
from datetime import datetime

#On récupère les informations de connexion au serveur fournis en ligne de commande
arguments = sys.argv[1:]
serveurName = arguments[0]
serveurPort = int(arguments[1])
#----------------------------------------------------
#Le relai se comporte comme un serveur
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #SOCK_STREAM = TCP
port = 5678
serverSocket.bind(('127.0.0.1',port)) 
serverSocket.listen(1) #ecoute sur le socket serveur
#----------------------------------------------
print("---------------------------------------------")
print(f"-----Relai PROXY démarré (port:{port}) -----")
print("---------------------------------------------")
#------------------------------------------------
def lecture_fichier_configuration():
    liste_config = []
    try:
        with open("config.txt","r") as f:
            for ligne in f.readlines():
                liste_config.append(ligne.replace("\n",""))
        return liste_config
    except FileNotFoundError:
        print("Fichier de configuration manquant")
        return []
    
def affichage_log(dlog):
    aff = "------------ LOG ACCES FICHIERS INTERDITS ------------------\n"
   
    for uri,dico in dlog.items():
        aff += f"Le fichier interdit  {uri} a été demandé {dico['nb_tentative']} par :\n"
        for i in range(len(dico['ip'])):
            aff +=  f"{dico['ip'][i]} le {dico['date'][i]}\n"
    aff += "------------------------------------------------------------\n"
    print(aff)
    

#on lit et stocke la liste des URI interdits
liste_config = lecture_fichier_configuration()
if liste_config:
    print("------ Liste des URI interdites ---------")
    for l in liste_config:
        print(l)
    print("-----------------------------------------")
dico_log = {}

while True:
    print("Je suis à l'écoute...")
    print("------------------------------------------")
    connectionSocket, address = serverSocket.accept() #ouverture socket datas
    print("Connexion de ",address," Tunnel TCP ouvert")
    try:
        requete = connectionSocket.recv(2048).decode('utf-8') #on garde recv car la requete est courte
        print("MESSAGE RECU DU CLIENT :",requete)
        commande = requete.split(" ")
        #print(commande)
        uri = commande[1] #on récupère le nom du fichier demandé
        #si l'URI figure parmi la liste des URI interdites
        if uri in liste_config:
            print(f"WARNING ! {uri} figure dans la liste des URI interdites !!!")
            message_length = len(uri) + 32
            rep = f"WARNING : {uri} est interdit d'accès." #de taille 32
            reponseHTTP = (
            "HTTP/1.1 400 Bad Request\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {message_length}\r\n\r\n"
            f"{rep}"
            )
            reponse = reponseHTTP.encode('utf-8')
            #on cree l'entrée dans le dictionnaire log
            # on récupère la date et l'heure actuelles
            maintenant = datetime.now() 
            # on la formater en chaîne de caractères
            date_heure_chaine = maintenant.strftime("%d/%m/%Y %H:%M:%S")
            #si cette URI a déjà été rencontrée, on met à jour les données la concernant
            if uri in dico_log:
                dico_log[uri]['ip'].append(address[0])
                dico_log[uri]['date'].append(date_heure_chaine)
                dico_log[uri]['nb_tentative']+=1
                #sinon on crée l'entrée
            else:
                dico_log[uri] = {'ip':[address[0]],'date':[date_heure_chaine],'nb_tentative':1}
            affichage_log(dico_log)             
        else:
            #Le relai se comporte maintenant comme un client et interroge le serveur
            clientSocket = socket(AF_INET,SOCK_STREAM) #TCP
            try:
                clientSocket.connect((serveurName,serveurPort)) #il se connecte au serveur
                clientSocket.send(requete.encode('utf-8'))
                reponse = get_block(clientSocket) #on récupère le message
                print("reponse reçue du serveur",reponse.decode('utf-8'))
            except ConnectionRefusedError:
                print("Impossible de se connecter au serveur.")
                reponse = "Le serveur est HS !".encode('utf-8')
            except ConnectionResetError:
                print("Connexion interrompue par le serveur.")
                reponse = "Erreur : Connexion interrompue.".encode('utf-8')
            finally:
                print("Fermeture du tunnel TCP")
                clientSocket.close()          
        #Le relai "redevient" serveur et transmets la réponse qu'il a reçue ou fabriquée au client
        put_block(connectionSocket,reponse) # car le fichier peut-être grand
    except Exception as e:
        print(f"Erreur avec le client : {e}")
    finally:
        connectionSocket.close()


