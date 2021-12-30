import socket
IPs = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None) if ':' not in i[4][0]]
print(IPs)