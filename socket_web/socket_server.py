import socketserver

from socketserver import BaseRequestHandler,TCPServer
from socketserver import ThreadingTCPServer

class EchoHandle(BaseRequestHandler):
    def handle(self):
        print ('Got connection from :',self.client_address)
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)

if __name__ == '__main__':
    server = ThreadingTCPServer(('',20000),EchoHandle)
    server.serve_forever()