from socket import socket,AF_INET,SOCK_STREAM

for i in range(10):
    s = socket(AF_INET,SOCK_STREAM)
    s.connect(('localhost',20000))
    s.send(b'hello clinet socket')

    recv = s.recv(8192)

    print ('recv :',recv)