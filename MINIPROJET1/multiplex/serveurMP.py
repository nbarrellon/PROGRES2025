from select import *
from socket import *


def get_local_ip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        # On se connecte à un serveur externe (non résolu) pour obtenir l'IP locale
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

my_poll = poll()
serverPort = 8080 #en lieu et place du port habituel 80
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('0.0.0.0', serverPort))  # '' signifie "toutes les interfaces réseau disponibles"
serverSocket.listen()
sockets = {serverSocket.fileno(): serverSocket}
# retrieve socket object from fileno
received = dict()
# bytes received from fileno, that are not yet processed
to_send = dict()
# bytes to be sent from fileno, that have been processed
while True:
    print("-----------------------------------------------")
    print("Serveur en écoute sur l'adresse IP", get_local_ip())
    print("Port d'écoute :",serverPort)
    print("----------------------------------------------")
    for fd, event in my_poll.poll():
        if event & (POLLHUP|POLLERR|POLLNVAL):
            received.pop(fd)
            to_send.pop(fd)
            my_poll.unregister(fd)
            del sockets[fd]
            sockets.pop(fd)
        elif sockets[fd] is serverSocket:
            connectionSocket, address = serverSocket.accept()
            sockets[connectionSocket.fileno()] = connectionSocket
            my_poll.register(connectionSocket,POLLIN)
        else:
            if event & POLLIN:
                try:
                    data = sockets[fd].recv(4096)
                    if not data:
                        sockets[fd].close()
                        continue
                    if fd in received:
                        received[fd] += data
                    else:
                        received[fd] = data
                    my_poll.modify(fd,POLLIN|POLLOUT)
                except Exception as e:
                    print(f"Erreur de socket : {e}")
                    sockets[fd].close()
                    continue
            if event & POLLOUT:
                data = received.pop(fd).decode("utf-8")
                data = data.upper().encode("utf-8")
                if fd in to_send:
                    data = to_send.pop(fd) + data
                n = sockets[fd].send(data)
                if n < len(data):
                    to_send[fd] = data[n:]
                else:
                    my_poll.modify(fd,POLLIN)