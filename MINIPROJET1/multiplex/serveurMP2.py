from select import *
from socket import *
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_local_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def cleanup_socket(fd, sockets, received, to_send, my_poll):
    """Nettoie les ressources associées à un socket."""
    if fd in received:
        received.pop(fd)
    if fd in to_send:
        to_send.pop(fd)
    if fd in sockets:
        sockets[fd]["socket"].close()
        del sockets[fd]
    my_poll.unregister(fd)

my_poll = poll()
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen()

# Structure pour stocker les sockets et leurs adresses
sockets = {serverSocket.fileno(): {"socket": serverSocket, "address": None}}
received = dict()  # Données reçues non traitées
to_send = dict()   # Données à envoyer

logging.info(f"Serveur en écoute sur l'adresse IP {get_local_ip()} ou 127.0.0.1, port {serverPort}")

while True:
    for fd, event in my_poll.poll():
        if event & (POLLHUP | POLLERR | POLLNVAL):
            logging.warning(f"Événement POLLHUP/POLLERR/POLLNVAL sur le socket {fd}")
            cleanup_socket(fd, sockets, received, to_send, my_poll)

        elif sockets[fd]["socket"] is serverSocket:
            # Accepter une nouvelle connexion
            connectionSocket, address = serverSocket.accept()
            fd_new = connectionSocket.fileno()
            sockets[fd_new] = {"socket": connectionSocket, "address": address}
            my_poll.register(fd_new, POLLIN)
            logging.info(f"Nouvelle connexion de {address}")

        else:
            if event & POLLIN:
                try:
                    data = sockets[fd]["socket"].recv(4096)
                    if not data:
                        logging.info(f"Connexion fermée par le client {sockets[fd]['address']}")
                        cleanup_socket(fd, sockets, received, to_send, my_poll)
                        continue

                    try:
                        decoded_data = data.decode('utf-8')
                    except UnicodeDecodeError:
                        decoded_data = data.decode('latin-1')  # Encodage de repli

                    logging.info(f"Requête reçue de {sockets[fd]['address']}: {decoded_data}")

                    if fd in received:
                        received[fd] += data
                    else:
                        received[fd] = data

                    my_poll.modify(fd, POLLIN | POLLOUT)

                except Exception as e:
                    logging.error(f"Erreur lors de la réception des données: {e}")
                    cleanup_socket(fd, sockets, received, to_send, my_poll)

            if event & POLLOUT:
                try:
                    data = received.pop(fd)
                    decoded_data = data.decode('utf-8')
                    processed_data = decoded_data.upper().encode('utf-8')

                    if fd in to_send:
                        processed_data = to_send.pop(fd) + processed_data

                    n = sockets[fd]["socket"].send(processed_data)

                    if n < len(processed_data):
                        to_send[fd] = processed_data[n:]
                    else:
                        my_poll.modify(fd, POLLIN)

                except Exception as e:
                    logging.error(f"Erreur lors de l'envoi des données: {e}")
                    cleanup_socket(fd, sockets, received, to_send, my_poll)
