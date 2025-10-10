#Nils BARRELLON 21401602
#Permet de dresser les statistiques d'une URI à partir du dictionnaire stocké par le Relai SNIFFEUR

from datetime import datetime

def decodage_reponse(reponse):
    status = reponse[9:12]
    answer = reponse[reponse.index("\r\n\r\n")+4:][:30]
    return status,answer

def statistiques(dico_log,uri):
    print('Statistiques envoyées au client :')
    if uri not in dico_log:
        message_length = len(uri) + 56
        reponse = f"{uri} n'a jamais été demandé au serveur. Pas de statistiques."
        reponseHTTP = (
        "HTTP/1.1 400 Bad Request\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {message_length}\r\n\r\n"
        f"{reponse}"
        )
    else:
        stat = dico_log[uri]
        reponse = "----------- Pour l'URI "+uri+" ----------------------------------\n"
        reponse += "Ressource demandée "+str(len(stat['ip']))+" fois\n"
        # on cree une liste de tuples (indice, date)
        dates_avec_indices = [(i, date) for i, date in enumerate(stat['date'])]
        # on trie la liste en utilisant la date comme clé de tri
        dates_triees = sorted(dates_avec_indices, key=lambda x: datetime.strptime(x[1], "%d/%m/%Y %H:%M:%S"))
        # date[1] la date ; date[0] l'indice dans la liste d'origine pour retrouver l'IP
        reponse += "-------------------------------------------------------------------------------\n"
        reponse += "date de demande      | IP du demandeur| Statut HTTP | Réponse\n"
        reponse += "-------------------------------------------------------------------------------\n"
        for date in dates_triees:
            ip = stat['ip'][date[0]]
            status, answer = decodage_reponse(stat['reponse'][date[0]])
            reponse += date[1]+"  | "+ip+" "*(15-len(ip))+"| "+status+"         |"+answer+"\n"
        reponse += "-----------------------------------------------------------------------------------\n"
        #formatage de la réponse HTTP.
        block_length = len(reponse)
        reponseHTTP = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {block_length}\r\n\r\n"
        f"{reponse}"
        )
    print(reponse)
    return reponseHTTP.encode('utf-8')