from select import *

while True:

    my_poll = poll()
    my_poll.register(serverSocket,POLLIN)
    sockets = {serverSocket.fileno(): serverSocket}
    # retrieve socket object from fileno
    for fd, event in my_poll.poll():
    if event & (POLLHUP|POLLERR|POLLNVAL):
    received.pop(fd)
    to_send.pop(fd)
    received = dict()
    # bytes received from fileno, that are not yet processed
    to_send = dict()
    my_poll.unregister(fd)
    del sockets[fd]
    # bytes to be sent from fileno, that have been processed
    sockets.pop(fd)