from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time
import sys
import dateutil.parser
import mysqlinterface
import mysql.connector
import structures as ds
import json

GET_FUNCTION_TOKEN_RANGES = {\
            'HD': '2', 'RD': '3', 'HT': '3', 'RT': '4',\
            'UI': '2,3', 'HI': '2,3',\
            'AL': '3-5', 'AT': '6', 'AI': '6',\
            'CL': '3-5', 'CT': '6', 'CI': '6'}
POST_FUNCTION_TOKEN_RANGES = {'D': '6', 'R': '4', 'H': '2', 'U': '2'}
PATCH_FUNCTION_TOKEN_RANGES = {'A': '4-6', 'C': '4-6'}
DELETE_FUNCTION_TOKEN_RANGES = {'A': '2', 'D': '5', 'R': '4', 'H': '2', 'U': '2'}

class HATSPersistentStorageRequestHandler(BaseHTTPRequestHandler):

    #When responsding to a request, the server instantiates a DeviceHubRequestHandler
    #and calls one of these functions on it.
    
    def do_GET(self):
        try:
            if self.validateGetRequest(self.path):
                queryType = self.path.strip('/').split('/')[0]
                if queryType == 'HD':
                    houseID = self.getHouseID(self.path)
                    body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID))
                    self.wfile.write(body)
                elif queryType == 'RD':
                    houseID = self.getHouseID(self.path)
                    roomID = self.getRoomID(self.path)
                    body = ds.DumpJsonList(self.server.sqldb.get_room_devices(houseID, roomID))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(body)
                elif queryType == 'HT':
                    houseID = self.getHouseID(self.path)
                    deviceType = self.getDeviceType(self.path)
                    body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID, deviceType))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(body)
                elif queryType == 'RT':
                    houseID = self.getHouseID(self.path)
                    roomID = self.getRoomID(self.path)
                    deviceType = self.getDeviceType(self.path)
                    body = ds.DumpJsonList(self.server.sqldb.get_room_devices(houseID, roomID, deviceType))
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(body)
                elif queryType == 'HI':
                    houseID = self.getHouseID(self.path)
                    blob = self.server.sqldb.get_house_data(houseID)
                    if blob is None or blob == '':
                        self.send_response(404)
                        self.end_headers()
                    else:
                        body=json.dumps({'version': 0, 'blob': blob})
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(body)
                elif queryType == 'UI':
                    userID = self.getUserID(self.path)
                    blob = self.server.sqldb.get_user_data(userID)
                    if blob is None or blob == '':
                        self.send_response(404)
                        self.end_headers()
                    else:
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(blob)
                else:
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
                queryType = self.path.strip('/').split('/')[0]
                if queryType == 'D':
                    houseID = self.getHouseID(self.path)
                    roomID = self.getRoomID(self.path)
                    deviceID = self.getDeviceID(self.path)
                    deviceType = self.getDeviceType(self.path)
                    data = self.readPayload()
                    print houseID
                    print roomID
                    print deviceID
                    print deviceType
                    print data
                    try:
                        self.server.sqldb.insert_room_device(ds.Device(houseID, deviceID,
                          deviceType, data, roomID)) 
                    except mysql.connector.errors.IntegrityError:
                        print 'updating'
                        self.server.sqldb.update_device(houseID, deviceID,
                            data, roomID)
                elif queryType == 'R':
                    houseID = self.getHouseID(self.path)
                    roomID = self.getRoomID(self.path)
                    data = self.readPayload()
                    try:
                        self.server.sqldb.insert_room(ds.Room(houseID, roomID,
                              data, ''))
                    except mysql.connector.errors.IntegrityError:
                        self.server.sqldb.update_room(houseID, roomID, data)
                elif queryType == 'H':
                    houseID = self.getHouseID(self.path)
                    data = self.readPayload()
                    try:
                        self.server.sqldb.insert_house(ds.House(houseID, data,
                              '', ''))
                    except mysql.connector.errors.IntegrityError:
                        self.server.sqldb.update_house(houseID, data)
                elif queryType == 'U':
                    userID = self.getUserID(self.path)
                    data = self.readPayload()
                    try:
                        self.server.sqldb.insert_user(ds.User(userID, data))
                    except mysql.connector.errors.IntegrityError:
                        self.server.sqldb.update_user(userID, data)
                self.server.sqldb.commit_changes()
                self.stubResponseOK()  
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()
    
    def readPayload(self):
        length = int(self.headers.getheader('content-length', 0))
        return self.rfile.read(length)

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
        try:
            if self.path.strip('/') == 'everything/for/testing/purposes':
                #buckle up, we're going nuclear
                self.server.sqldb.reset_tables()
                self.server.sqldb.commit_changes()
                self.stubResponseOK()
                return
            if self.validateDeleteRequest(self.path): 
                queryType = self.path.strip('/').split('/')[0]
                if queryType == 'A':
                    userID = self.getUserID(self.path)
                    self.server.sqldb.delete_user(userID)
                if queryType == 'D':
                    houseID = self.getHouseID(self.path)
                    roomID = self.getRoomID(self.path)
                    deviceID = self.getDeviceID(self.path)
                    self.server.sqldb.delete_device(houseID, deviceID, roomID)
                if queryType == 'R':
                    houseID = self.getHouseID(self.path)
                    roomID = self.getRoomID(self.path)
                    self.server.sqldb.delete_room(houseID, roomID)
                if queryType == 'H':
                    houseID = self.getHouseID(self.path)
                    self.server.sqldb.delete_house(houseID)
                self.server.sqldb.commit_changes()
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def validateDeleteRequest(self, path):
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in DELETE_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), DELETE_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

    def getHouseID(self, path):
        tokenizedPath = path.strip('/').split('/')
        if tokenizedPath[0] == 'HD' or tokenizedPath[0] == 'RD' or tokenizedPath[0] == 'HT' or tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'HI' or tokenizedPath[0] == 'D' or tokenizedPath[0] == 'R' or tokenizedPath[0] == 'H':
            return tokenizedPath[1]
        elif (tokenizedPath[0] == 'AL' and len(tokenizedPath) > 3) or tokenizedPath[0] == 'CL' or (tokenizedPath[0] == 'A' and len(tokenizedPath) >2) or tokenizedPath[0] == 'C':
            return tokenizedPath[3]
        elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
            return tokenizedPath[4]
        else:
            self.send_response(400)

    def getUserID(self, path):
        tokenizedPath = path.strip('/').split('/')
        if tokenizedPath[0] == 'UI' or tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI' or tokenizedPath[0] == 'U' or tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C':
            return tokenizedPath[1]
        else:
            self.send_response(400)
        
    def getRoomID(self,path):
        tokenizedPath = path.strip('/').split('/')
        if tokenizedPath[0] == 'RD' or tokenizedPath[0] == 'RT':
            return tokenizedPath[2]
        elif tokenizedPath[0] == 'AL' and len(tokenizedPath) > 3:
            return tokenizedPath[4]
        elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
            return tokenizedPath[5]
        elif tokenizedPath[0] == 'D' or tokenizedPath[0] == 'R':
            return tokenizedPath[3]
        elif (tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C') and len(tokenizedPath) > 4:
            return tokenizedPath[5]
	elif tokenizedPath[0] == 'A':
            return tokenizedPath[1]
        else:
            self.send_response(400)

    def getDeviceID(self, path):
        tokenizedPath = path.strip('/').split('/')
        if tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CI':
            return tokenizedPath[3]
        elif tokenizedPath[0] == 'D' and len(tokenizedPath) > 5:
            return tokenizedPath[5]
        elif tokenizedPath[0] == 'D':#second d request
            return tokenizedPath[4]
        elif (tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C') and len(tokenizedPath) > 4:
            return tokenizedPath[4]
        else:
            self.send_response(400)
    
    def getDeviceType(self, path):
        tokenizedPath = path.strip('/').split('/')
        if tokenizedPath[0] == 'HT':
            return tokenizedPath[2]
        elif tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'CT': 
            return tokenizedPath[3]
        elif tokenizedPath[0] == 'D':
            return tokenizedPath[4]
        else:
            self.send_response(400)

    def getVersion(self, path):
        tokenizedPath = self.strip('/').split('/')
        if tokenizedPath[0] == 'D':
            return tokenizedPath[2]
        elif tokenizedPath[0] == 'R':
            return tokenizedPath[2]
        else:
            self.send_response(400)

    def getTimeFrame(self, path):
        tokenizedPath = self.strip('/').split('/')
        if tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI' or (tokenizedPath == 'A' and  len(tokenizedPath) > 2) or tokenizedPath[0] == 'C':
            return dateutil.parser.parse(tokenizedPath[2])
        else:
            self.send_response(400)


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
        self.sqldb = mysqlinterface.MySQLInterface('matthew', 'password', 'test3')

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
    LISTEN_PORT = 8081
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

