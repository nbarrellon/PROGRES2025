Exercice 1

Version très simpliste du relai : 
- il écoute le client (se comporte comme un serveur)
- s'il reçoit une requête, il la transmet au serveur (se comporte comme un client).
- s'il reçoit une réponse du serveur, il transmet cette réponse au client  
    sinon il envoie un message d'erreur (se comporte comme un serveur).

Tourne avec plusieurs clients en simultané (via des threads)

Pour cette version basique, on suppose que les messages sont du texte de longueur raisonnable (<2048 octets). 
=> utilisation de send et recv(2028)

---------------------------------------------------------------------------------------

Exercice 2 Pour cet exercice, le code du serveur est inchangé (il cherche le fichier et 
renvoie son contenu dans une réponse HTTP. Si le fichier est introuvable, il renvoie un message d'erreur 404
dans sa réponse HTTP.)

1) CACHE
L'ensemble tourne. Le cache conserve bien les réponses correspondant aux différentes requêtes pour ne pas les
redemander au serveur si jamais mais... uniquement pour des fichiers texte (.txt). En effet, je me suis heurté 
à un souci quand j'ai essayé de ré-écrire un fichier PDF envoyé par le serveur par exemple. 
Certains octets ne pouvaient être encodés en utf-8 et donc impossibles à écrire dans un fichier.

J'ai tenté de discriminer fichier txt et autres fichiers mais je n'ai pas réussi :-(

Le client enregiste le contenu de la réponse HTTP du serveur dans un fichier

nom_du_fichier_copy.txt dans le répertoire courant.

2) SNIFFEUR
Tout semble fonctionner. L'appel aux statistiques se fait lors de la requête de l'URI 
en ajoutant STATS dans le fichier demandé
Quel fichier voulez-vous ? film1.txt STATS
Si le relai détecte cette commande, il n'appelle pas le serveur mais construit une réponse des statistiques
concernant ce fichier (s'il existe) et renvoie une réponse HTTP contenant ces STATS
Le client enregistre ces stats dans une fichier film1_STATS.txt dans le répertoire courant.

3) PROXY
Tout semble fonctionner. Une réponse 400 Bad request est demandée si un fichier interdit est demandé.
Le fichier de log s'affiche donnant combien de fois une URI interdite a été demandée et par qui à quelle heure

4) TUNNEL DE RELAI.
Tout semble fonctionner. 
Pour tirer profit des fonctionnalités de chaque relai, il convient de les lancer "dans le bon ordre !"
- Le relai CACHE est connecté au serveur (127.0.0.1,8080)
- Le relai PROXY est connecté au relai CACHE (127.0.0.1,55553)
- Le relai SNIFFEUR est connecté au relai PROXY (127.0.0.1,55552) : cela permet de bien ajouter 1 quand on demande une URI interdite
et permet de dresser des stats sur ce fichier tout de même
- Le client est connecté au relai SNIFF (127.0.0.1 55551) 

Pour respecter cet ordre dans le tunnel, j'ai supprimé la lecture de la ligne de commande pour graver dans le dur 
à quel IP,port doit se connecter chaque relai.
----------------------------------------------------------------------------------------
