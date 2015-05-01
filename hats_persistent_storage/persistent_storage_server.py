from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time
import sys
import dateutil.parser
import mysqlinterface
import structures as ds
from structures import Device, User, Room, House, UserAction, CompAction
import json
import parser
from sys import argv

class HATSPersistentStorageRequestHandler(BaseHTTPRequestHandler):

    #When responsding to a request, the server instantiates a DeviceHubRequestHandler
    #and calls one of these functions on it.
    
    def do_GET(self):
        try:
            if not parser.validateGetRequest(self.path):
                return self.http_invalid_request()

            queryType = self.path.strip('/').split('/')[0]
            if queryType == 'HD':
                houseID = parser.getHouseID(self.path)
                if not houseID:
                    return self.http_invalid_request()
                body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID))
                return self.http_ok(body, 'Content-Type', 'application/json')

            elif queryType == 'RD':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                if not houseID or not roomID:
                    return self.http_invalid_request()
                body = ds.DumpJsonList(self.server.sqldb.get_room_devices(houseID, roomID))
                return self.http_ok(body, 'Content-Type', 'application/json')
                houseID = parser.getHouseID(self.path)
                deviceType = parser.getDeviceType(self.path)
                if not houseID or not deviceType:
                    return self.http_invalid_request()
                body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID, deviceType))
                return self.http_ok(body, 'Content-Type', 'application/json')

            elif queryType == 'RT':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                deviceType = parser.getDeviceType(self.path)
                if not houseID or not roomID or not deviceType:
                    return self.http_invalid_request()
                body = ds.DumpJsonList(self.server.sqldb.get_room_devices(houseID, roomID, deviceType))
                return self.http_ok(body, 'Content-Type', 'application/json')

            elif queryType == 'HT':
                houseID = parser.getHouseID(self.path)
                deviceType = parser.getDeviceType(self.path)
                if not houseID or not deviceType:
                    return self.http_invalid_request();
                body = ds.DumpJsonList(self.server.sqldb.get_house_devices(houseID, deviceType))
                return self.http_ok(body, 'Content-Type', 'application/json')

            elif queryType == 'BH':
                houseID = parser.getHouseID(self.path)
                if not houseID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_house_data(int(houseID))
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob, 'Content-Type', 'application/json')

            elif queryType == 'BU':
                userID = parser.getUserID(self.path)
                if not userID:
                    return self.http_invalid_request();
                blob = self.server.sqldb.get_user_data(userID)
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob)

            elif queryType == 'BR':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                if not houseID or not roomID:
                    return self.http_invalid_request();
                blob = self.server.sqldb.get_room_data(houseID,roomID)
                if blob is None or blob == '':
                    return self.http_resource_not_found();
                return self.http_ok(blob)

            elif queryType == 'BD':
                houseID = parser.getHouseID(self.path)
                deviceID = parser.getDeviceID(self.path)
                roomID = parser.getRoomID(self.path)
                if not houseID or not deviceID or not roomID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_device_data(houseID,deviceID,roomID)
                if blob is None or blob == '':
                    return self.http_resource_not_found()

                return self.http_ok(blob)

            elif queryType == 'DD':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                deviceID = parser.getDeviceID(self.path)
                if not houseID or not roomID or not deviceID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_device_data(houseID,deviceID,roomID)
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                body = self.server.sqldb.get_device_data(houseID,deviceID,roomID)
                return self.http_ok(body, 'Content-Type', 'application/json')

            elif queryType == 'AL':
                userID = parser.getUserID(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                if not userID or not timeFrame:
                    return self.http_invalid_request()
                blob = ds.DumpJsonList(self.server.sqldb.get_user_actions(userID, houseID, roomID, None, timeFrame[0], timeFrame[1]))
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob, 'Content-Type', 'application/json')

            elif queryType == 'AT':
                userID = parser.getUserID(self.path)
                deviceType = parser.getDeviceType(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                if not userID or timeFrame or deviceType or houseID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_user_actions(userID, houseID, roomID, None, timeFrame[0], timeFrame[1])
                if blob is None or blob == '':
                    return self.http_ok(body)
                return self.http_ok(blob, 'Content-Type', 'application/json')

            elif queryType == 'AI':
                userID = parser.getUserID(self.path)
                deviceID = parser.getDeviceID(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                if not userID or timeFrame or deviceID or houseID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_user_actions(userID, houseID, roomID, deviceID, timeFrame[0], timeFrame[1])
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob, 'Content-Type', 'application/json')

            elif queryType == 'CL':
                userID = parser.getUserID(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                if not userID or not timeFrame:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_comp_actions(userID, houseID, roomID, None, timeFrame[0], timeFrame[1])
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob, 'Content-Type', 'application/json')

            elif queryType == 'CT':
                userID = parser.getUserID(self.path)
                deviceType = parser.getDeviceType(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                if not userID or timeFrame or deviceType or houseID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_comp_actions(userID, houseID, roomID, None, timeFrame[0], timeFrame[1])
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob, 'Content-Type', 'application/json')

            elif queryType == 'CI':
                userID = parser.getUserID(self.path)
                deviceID = parser.getDeviceID(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                if not userID or timeFrame or deviceID or houseID:
                    return self.http_invalid_request()
                blob = self.server.sqldb.get_comp_actions(userID, houseID, roomID, deviceID, timeFrame[0], timeFrame[1])
                if blob is None or blob == '':
                    return self.http_resource_not_found()
                return self.http_ok(blob, 'Content-Type', 'application/json')

            else:
                self.http_invalid_request()
        except:
            #For any other uncaught internal error, respond HTTP 500:
            e = sys.exc_info()
            print e
            self.http_internal_error()

    def do_POST(self):
        try:
          if not parser.validatePostRequest(self.path):
              return self.http_invalid_request()

          queryType = self.path.strip('/').split('/')[0]
          if queryType == 'RESET':
              self.server.sqldb.reset_tables()
              return self.http_ok()

          elif queryType == 'D':
              houseID = parser.getHouseID(self.path)
              roomID = parser.getRoomID(self.path)
              deviceType = parser.getDeviceType(self.path)
              if not houseID or not roomID or not deviceType:
                  return self.http_invalid_request()
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              newDevice = Device(houseID, None, deviceType, data, roomID)
              deviceID = ''
              if roomID == 0:
                  deviceID = self.server.sqldb.insert_house_device(newDevice)
              else:
                  deviceID = self.server.sqldb.insert_room_device(newDevice)
              return self.http_ok(deviceID, 'Content-Type', 'text')

          elif queryType == 'R':
              houseID = parser.getHouseID(self.path)
              if not houseID:
                  return self.http_invalid_request()
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              newRoom = Room(houseID, None, data, None)
              roomID = self.server.sqldb.insert_room(newRoom)
              return self.http_ok(roomID, 'Content-Type', 'text')

          elif queryType == 'H':
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              newHouse = House(None, data, None, None)
              try:
                  houseID = self.server.sqldb.insert_house(newHouse)
              except:
                  self.send_response(333)
                  self.end_headers()
              return self.http_ok(houseID, 'Content-Type', 'text')

          elif queryType == 'U':
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              newUser = User(None, data)
              userID = self.server.sqldb.insert_user(newUser)
              return self.http_ok(userID, 'Content-Type', 'text')
          elif queryType == 'UU':
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              userID = parser.getUserID(self.path)

              # Ensure data is already there.
              stored = self.server.sqldb.get_user_data(userID)
              if stored is None or stored == '':
                  return self.http_resource_not_found()

              # Update the user data and send a 200.
              self.server.sqldb.update_user(userID, data)
              return self.http_ok()
            
          elif queryType == 'UH':
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              houseID = parser.getHouseID(self.path)

              # Ensure data is already there.
              stored = self.server.sqldb.get_house_data(houseID)
              if stored is None or stored == '':
                  return self.http_resource_not_found()

              # Update the house data and send a 200.
              self.server.sqldb.update_house(houseID, data)
              return self.http_ok()

          elif queryType == 'UR':
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              houseID = parser.getHouseID(self.path)
              roomID = parser.getRoomID(self.path)

              # Ensure data is already there.
              stored = self.server.sqldb.get_room_data(houseID, roomID)
              if stored is None or stored == '':
                  return self.http_resource_not_found()

              # Update the room data and send a 200.
              self.server.sqldb.update_room(houseID, roomID, data)
              return self.http_ok()

          elif queryType == 'UD':
              length = int(self.headers.getheader('content-length', 0))
              data = self.rfile.read(length)
              houseID = parser.getHouseID(self.path)
              roomID = parser.getRoomID(self.path)
              deviceID = parser.getDeviceID(self.path)

              # Ensure data is already there.
              stored = self.server.sqldb.get_device_data(houseID,
                  deviceID, roomID)
              if stored is None or stored == '':
                  return self.http_resource_not_found()

              # Update the device data and send a 200.
              self.server.sqldb.update_device(houseID, deviceID, data, roomID)
              return self.http_ok()
        except:
            e = sys.exc_info()
            print e
            self.http_internal_error()

    def do_PATCH(self):
        try:
            if not parser.validatePatchRequest(self.path):
                return self.http_invalid_request()

            queryType = self.path.strip('/').split('/')[0]
            if queryType == 'A':
                userID = parser.getUserID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                deviceID = parser.getDeviceID(self.path)
                if not userID or not timeFrame or not houseID or not roomID or not deviceID:
                  return self.http_invalid_request()
                length = int(self.headers.getheader('content-length', 0))
                data = self.rfile.read(length)
                newUserAction = UserAction(userID, timeFrame, houseID, roomID, deviceID, data)
                self.server.sqldb.insert_user_action(newUserAction)
                return self.http_ok()
            elif queryType == 'C':
                userID = parser.getUserID(self.path)
                timeFrame = parser.getTimeFrame(self.path)
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                deviceID = parser.getDeviceID(self.path)
                if not userID or not timeFrame or not houseID or not roomID or not deviceID:
                  return self.http_invalid_request()
                length = int(self.headers.getheader('content-length', 0))
                data = self.rfile.read(length)
                newCompAction = CompAction(userID, timeFrame, houseID, roomID, deviceID, data)
                self.server.sqldb.insert_comp_action(newCompAction)
                return self.http_ok()
            else:
                self.http_invalid_request()
        except:
            e = sys.exc_info()
            print e
            self.http_internal_error()

    def do_DELETE(self):
        try:
            if not parser.validateDeleteRequest(self.path):
                return self.http_invalid_request()

            queryType = self.path.strip('/').split('/')[0]
            if queryType == 'A':
                userID = parser.getUserID(self.path)
                if not userID:
                    return self.http_invalid_request()
                self.server.sqldb.delete_user(userID)
                return self.http_ok()

            elif queryType == 'D':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                deviceID = parser.getDeviceID(self.path)
                if not houseID or not roomID or not deviceID:
                    return self.http_invalid_request()
                self.server.sqldb.delete_device(houseID, deviceID, roomID)
                return self.http_ok()

            elif queryType == 'R':
                houseID = parser.getHouseID(self.path)
                roomID = parser.getRoomID(self.path)
                if not houseID or not roomID:
                    return self.http_invalid_request()
                self.server.sqldb.delete_room(houseID, roomID)
                return self.http_ok()

            elif queryType == 'H':
                houseID = parser.getHouseID(self.path)
                if not houseID:
                    return self.http_invalid_request()
                self.server.sqldb.delete_house(houseID)
                return self.http_ok()

            else:
                self.http_invalid_request()
        except:
            e = sys.exc_info()
            print e
            self.http_internal_error()


    def http_ok(self, body=None, htype=None, hdata=None):
        self.send_response(200)
        if not (htype is None or hdata is None):
            self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if not body is None:
            self.wfile.write(body)


    def http_invalid_request(self):
        self.send_response(400)
        self.end_headers()


    def http_resource_not_found(self):
        self.send_response(404)
        self.end_headers()


    def http_internal_error(self):
        self.send_response(500)
        self.end_headers()


class HATSPersistentStorageServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass, user, password, database):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.shouldStop = False
        self.timeout = 1
        self.sqldb = mysqlinterface.MySQLInterface(user, password, database)

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
    script, port, user, password, database = argv
    
    server = HATSPersistentStorageServer(('', int(port)),
        HATSPersistentStorageRequestHandler, user, password, database)
    serverThread = serveInBackground(server)
    try:
        while serverThread.isAlive():
            time.sleep(120)
    except KeyboardInterrupt:
        print 'Attempting to stop server (timeout in 30s)...'
        server.shouldStop = True
        serverThread.join(30)
        if serverThread.isAlive():
            print 'WARNING: Failed to gracefully halt server.'

