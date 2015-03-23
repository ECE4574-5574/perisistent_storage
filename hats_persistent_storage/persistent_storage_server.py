from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time
import sys

GET_FUNCTION_TOKEN_RANGES = {\
            'HD': '2', 'RD': '3', 'HT': '3', 'RT': '4',\
            'UI': '2,3', 'HI': '2,3',\
            'AL': '3-5', 'AT': '6', 'AI': '6',\
            'CL': '3-5', 'CT': '6', 'CI': '6'}
POST_FUNCTION_TOKEN_RANGES = {'D': '5', 'R': '4', 'H': '2', 'U': '2'}
PATCH_FUNCTION_TOKEN_RANGES = {'A': '4-6', 'C': '4-6'}

class HATSPersistentStorageRequestHandler(BaseHTTPRequestHandler):

    #When responsding to a request, the server instantiates a DeviceHubRequestHandler
    #and calls one of these functions on it.
    
    def do_GET(self):
        try:
            if self.validateGetRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            #For any other uncaught internal error, respond HTTP 500:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()
    
    def validateGetRequest(self, path): 
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in GET_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), GET_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

    def do_POST(self):
        try:
            if self.validatePostRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def validatePostRequest(self, path):
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in POST_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), POST_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))
    
    def do_PATCH(self):
        try:
            if self.validatePatchRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def validatePatchRequest(self, path):
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in PATCH_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), PATCH_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))
    
    def do_DELETE(self):
        self.send_response(200)
        self.end_headers()

    def stubResponseOK(self):
        self.send_response(200)
        self.end_headers()

    def stubResponseBadReq(self):
        self.send_response(400)
        self.end_headers()

    def stubResponseInternalErr(self):
        self.send_response(500)
        self.end_headers()

class HATSPersistentStorageServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.shouldStop = False
        self.timeout = 1

    def serve_forever (self):
        while not self.shouldStop:
            self.handle_request()

def isInRange(i, strRange):
    if '+' in strRange:
        min = int(strRange.split('+')[0])
        return i >= min

    allowable = []
    for onePart in strRange.split(','):
        if '-' in onePart:
            lo, hi = onePart.split('-')
            lo, hi = int(lo), int(hi)
            allowable.extend(range(lo, hi+1))
        else:
            allowable.append(int(onePart))
    
    return i in allowable

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

