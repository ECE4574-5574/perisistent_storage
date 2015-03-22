from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time

class HATSPersistentStorageRequestHandler(BaseHTTPRequestHandler):

    #When responsding to a request, the server instantiates a DeviceHubRequestHandler
    #and calls one of these functions on it.
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Hello World')
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
    
    def do_PATCH(self):
        self.send_response(200)
        self.end_headers()
    
    def do_DELETE(self):
        self.send_response(200)
        self.end_headers()

class HATSPersistentStorageServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.shouldStop = False
        self.timeout = 1

    def serve_forever (self):
        while not self.shouldStop:
            self.handle_request()

def runServer(server):
    server.serve_forever()

## Starts a server on a background thread.
#  @param server the server object to run.
#  @return the thread the server is running on.
#          Retain this reference because you should attempt to .join() it before exiting.
def serveInBackground(server):
    thread = threading.Thread(target=runServer, args =(server,))
    thread.start()
    return thread


if __name__ == "__main__":
    LISTEN_PORT = 8080
    server = HATSPersistentStorageServer(('',LISTEN_PORT), HATSPersistentStorageRequestHandler)
    serverThread = serveInBackground(server)
    try:
        while serverThread.isAlive():
            print 'Serving...'
            time.sleep(10)
            print 'Still serving...'
            time.sleep(10)
    except KeyboardInterrupt:
        print 'Attempting to stop server (timeout in 30s)...'
        server.shouldStop = True
        serverThread.join(30)
        if serverThread.isAlive():
            print 'WARNING: Failed to gracefully halt server.'

