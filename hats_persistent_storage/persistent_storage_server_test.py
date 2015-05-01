import unittest
import httplib
import persistent_storage_server as pss
import mysqlinterface as inter
import ast
from time import sleep
from structures import *

class PersistentStorageServertest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.init = 0
        print "Starting!"
        self.user = "mysql"
        self.password = ""
        self.database = "test_database"
        self.server = pss.HATSPersistentStorageServer(('',0),
            pss.HATSPersistentStorageRequestHandler, self.user, self.password, self.database)
        self.port = self.server.socket.getsockname()[1]
        self.thread = pss.serveInBackground(self.server)
        self.conn = httplib.HTTPConnection('localhost', self.port)


    @classmethod
    def tearDownClass(self):
        print "Tearing down server"
        self.server.shouldStop = True
        self.thread.join(5)

   
    def setUp(self):
        print "new test! Resetting database..."
        self.conn.request("POST", "RESET")
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()    


    def testEmptyQueries(self):
        self.conn.request("POST", "RESET")
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        self.conn.request('GET', 'BH/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        resp.read()
        self.conn.request('GET', 'BU/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        resp.read()
        self.conn.request('GET', 'BR/1/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        resp.read()
        self.conn.request('GET', 'BD/1/1/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        resp.read()

    def testModifyQueries(self):
        user = User(None, "OBAMA")
        house = House(None, "pet home", None, None)
        room = Room(1, None, "cat room", None)
        device = Device(1, None, 1, "cat1")
        newData = "MODIFIED"

        # Post a user and store it's ID
        self.conn.request('POST', 'U', user._data)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        user._user_id = resp.read()
        # Modify user data
        self.conn.request('POST', 'UU/' + user._user_id, newData)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        # Verify the user has posted correctly.
        self.conn.request('GET', 'BU/' + user._user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), newData)

        # Post a house and store it's ID
        self.conn.request('POST', 'H', house._data)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        house._house_id = resp.read()
        # Modify house data
        self.conn.request('POST', 'UH/' + house._house_id, newData)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        # Verify the house has posted correctly.
        self.conn.request('GET', 'BH/' + house._house_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), newData)

        # Post a room and store it's ID
        self.conn.request('POST', 'R/' + house._house_id, room._data)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        room._room_id = resp.read()
        # Modify room data
        self.conn.request('POST', 'UR/' + house._house_id + '/' + room._room_id, newData)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        # Verify the room has posted correctly.
        self.conn.request('GET', 'BR/' + house._house_id + '/' + room._room_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), newData)

        # Post a device and store it's ID
        self.conn.request('POST', 'D/' + house._house_id + '/' + room._room_id +
            '/' + '1', device._data)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        device._device_id = resp.read()
        # Modify device data
        self.conn.request('POST', 'UD/' + house._house_id + '/' + room._room_id
            + '/' + device._device_id, newData)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        # Verify the device has posted correctly.
        self.conn.request('GET', 'BD/' + house._house_id + '/' + room._room_id +
            '/' + device._device_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), newData)


    def testDayInLifeQueries(self):
        house1 = House(None, "pet home", None, None)

        room1 = Room(1, None, "cat room", None)
        room2 = Room(1, None, "dog room", None)
        h1rooms = [room1, room2]

        dev1 = Device(1, None, 1, "cat1")
        dev2 = Device(1, None, 2, "cat2")
        dev3 = Device(1, None, 1, "dog1")
        dev4 = Device(1, None, 2, "dog2")
        dev5 = Device(1, None, 1, "monkey1")
        dev6 = Device(1, None, 2, "monkey2")
        r1devs = [dev1, dev2]
        r2devs = [dev3, dev4]
        h1devs = [dev5, dev6]

        users = [User(None, "OBAMA"), User(None, "OSAMA")]
        for user in users:
            # Post a user and store it's ID
            self.conn.request('POST', 'U', user._data)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            user._user_id = resp.read()

            # Verify the user has posted correctly.
            self.conn.request('GET', 'BU/' + user._user_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), user._data)

            # Modify user data
            user._data = "NEWDATA" + user._user_id
            self.conn.request('POST', 'UU/' + user._user_id, user._data)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)

            # Verify the user has posted correctly.
            self.conn.request('GET', 'BU/' + user._user_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), user._data)

        # Post a house and store it's ID
        self.conn.request('POST', 'H', house1._data)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        house1._house_id = resp.read()

        # Verify the house has posted correctly.
        self.conn.request('GET', 'BH/' + house1._house_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), house1._data)

        # post all h1 rooms and get their id's
        # Test inserting and extracting rooms.
        for room in h1rooms:
            room._house_id = house1._house_id
            self.conn.request('POST', 'R/' + str(room._house_id), room._data)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            room._room_id = resp.read()

            self.conn.request('GET', 'BR/' + str(house1._house_id) + \
                '/' + str(room._room_id))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), room._data)

        # Insert and get all ID's for devices in room2.
        for dev in r1devs:
            dev._house_id = room1._house_id
            dev._room_id = room1._room_id

            self.conn.request('POST', 'D/' + str(dev._house_id) + '/' +
                str(dev._room_id) + '/' + str(dev._device_type), dev._data)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            dev._device_id = resp.read()

            self.conn.request('GET', 'BD/' + str(dev._house_id) + \
                '/' + str(dev._room_id) + '/' + str(dev._device_id))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), dev._data)

            self.conn.request('GET', 'DD/' + str(dev._house_id) + \
                '/' + str(dev._room_id) + '/' + str(dev._device_id))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), dev._data)

        # Insert and get all ID's for devices in room2.
        for dev in r2devs:
            dev._house_id = room2._house_id
            dev._room_id = room2._room_id

            self.conn.request('POST', 'D/' + str(dev._house_id) + '/' +
                str(dev._room_id) + '/' + str(dev._device_type), dev._data)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            dev._device_id = resp.read()

            self.conn.request('GET', 'BD/' + str(dev._house_id) + \
                '/' + str(dev._room_id) + '/' + str(dev._device_id))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), dev._data)

        # Insert and get all ID's for devices directly in the house.
        for dev in h1devs:
            dev._house_id = room2._house_id
            dev._room_id = 0

            self.conn.request('POST', 'D/' + str(dev._house_id) + '/' +
                str(dev._room_id) + '/' + str(dev._device_type), dev._data)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            dev._device_id = resp.read()

            self.conn.request('GET', 'BD/' + str(dev._house_id) + \
                '/' + str(dev._room_id) + '/' + str(dev._device_id))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), dev._data)

            self.conn.request('GET', 'DD/' + str(dev._house_id) + \
                '/' + str(dev._room_id) + '/' + str(dev._device_id))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), dev._data)



    # API calls for HOUSE
    def testDayInLifeQueries1(self):
            self.conn.request('GET', 'BH/')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 400)

            self.conn.request('POST', 'H', 'House1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            house1_id = resp.read()

            self.conn.request('POST', 'H', 'House2')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            house2_id = resp.read()

            self.conn.request('GET', 'BH/' + house1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), 'House1')

            self.conn.request('GET', 'BH/' + house2_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), 'House2')

            self.conn.request('DELETE', 'H/' + house1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            
            self.conn.request('GET', 'BH/' + house1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 404)
            
    
    # API calls for DEVICE
    def testDayInLifeQueries2(self):
         
            self.conn.request('POST', 'H', 'House')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            house1 = resp.read()  


            self.conn.request('POST', 'R/'+ house1, 'Room')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            Room1_id = resp.read()
   
            device_type1 = 1
            device_type2 = 4
            self.conn.request('POST', 'D/' + house1 + '/' + Room1_id + '/' + str(device_type1) , "Device") 
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            device_id = resp.read()
       	    print device_id
  
            self.conn.request('GET', 'HD/' + house1)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), '[{"device-id": ' + device_id + ', "device-type": 1, "blob": "Device"}]')

    
            self.conn.request('POST', 'D/' + house1 + '/' + Room1_id + '/' + str(device_type2) , 'Light1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            light1_id = resp.read()
 
            self.conn.request('POST', 'D/' + house1 + '/' + Room1_id + '/' + str(device_type2) , 'Light2')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            light2_id = resp.read()
 
            self.conn.request('POST', 'D/' + house1 + '/' + Room1_id + '/' + str(device_type2) , 'Light3')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            light3_id = resp.read()
 
            self.conn.request('GET', 'HT/' + house1 + '/' + str(device_type2))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), '[{"device-id": ' + light1_id + ', "device-type": 4, "blob": "Light1"}' + ', {"device-id": ' + light2_id + ', "device-type": 4, "blob": "Light2"}' + ', {"device-id": ' + light3_id + ', "device-type": 4, "blob": "Light3"}]' )
    
            self.conn.request('GET', 'RT/' + house1 + '/' + Room1_id + '/' + str(device_type2))
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), '[{"device-id": ' + light1_id + ', "device-type": 4, "blob": "Light1"}' + ', {"device-id": ' + light2_id + ', "device-type": 4, "blob": "Light2"}' + ', {"device-id": ' + light3_id + ', "device-type": 4, "blob": "Light3"}]' )
    
            self.conn.request('GET', 'DD/' + house1 + '/' + Room1_id + '/' + light1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), 'Light1')
           
            self.conn.request('DELETE', 'D/' + house1 + '/' + Room1_id + '/' + light1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)

            self.conn.request('GET', 'DD/' + house1 + '/' + Room1_id + '/' + light1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 404)
            

     # API calls for retrieving blobs
    def testDayInLifeQueries3(self):
                
            self.conn.request('POST', 'H', 'House1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            house1_id = resp.read()
     
            self.conn.request('POST', 'R/'+ house1_id, 'Room1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            Room1_id = resp.read()

            self.conn.request('GET', 'BR/' + house1_id + '/' + Room1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), 'Room1')

            
            self.conn.request('DELETE', 'R/' + house1_id + '/' + Room1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)

            self.conn.request('GET', 'BR/' + house1_id + '/' + Room1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 404)
           
    def testDayInLifeQueries4(self):

        self.conn.request('POST', 'U', 'USERDATA1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        user1_id = resp.read()
        
        self.conn.request('GET', 'BU/' + user1_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), 'USERDATA1')
       
        self.conn.request('POST', 'UU/' + user1_id, 'NEWDATA')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        
        self.conn.request('GET', 'BU/' + user1_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), 'NEWDATA')

    def testGoodGetDeviceQueries(self):

        self.conn.request('GET', 'HD/house47/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'RD/house47/atrium')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'HT/house47/lights')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'RT/house47/atrium/lights')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

    def testGoodGetUserQuery(self):
        self.conn.request('GET', 'BU/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)

        self.conn.request('POST', 'U', 'USER2036')
        resp = self.conn.getresponse()
        
        user_id = resp.read()

        self.conn.request('GET', 'BU/' + user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.read(), 'USER2036') 

        self.conn.request('DELETE', 'A/' + user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'BU/' + user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        

    def testGoodGetHouseQuery(self):
        self.conn.request('GET', 'BH/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        
        self.conn.request('POST', 'H', 'house47')
        resp = self.conn.getresponse()
        house47_id = resp.read()
       
        self.conn.request('GET', 'BH/' + house47_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), 'house47')


    def testGoodGetLogQueries(self):
        self.conn.request('GET', 'AL/user47/timestamp/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'AL/user47/timestamp/house24/ballroom')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'AT/user21/timestamp/lightbulb/house10/ballroom')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'AI/user10/timestamp/light41/house10/ballroom')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'CL/user10/timestamp/house10/ballroom')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'CT/user40/timestamp/lightbulb/house14/ballroom')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'CI/user10/timestamp/hlight41/house10/ballroom')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

    def testBadGetQueries(self):
        self.conn.request('GET', 'boguspath')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('GET', 'HD/house47/extratoken')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('GET', 'HD/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

    def testGoodPostQueries(self):
        self.conn.request('POST', 'D/house2021/15/light/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('POST', 'R/house2022')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        
        self.conn.request('POST', 'H', "stuffs")
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('POST', 'U', "garblegarble")
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

    def testBadPostQueries(self):
        self.conn.request('POST', 'bogusPath')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'D/notenoughtokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'D/houseID/ver/room/devicetype/device/extratokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'R')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'R/houseID/toomanytokens/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'H/toomanytokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'U/toomanytokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

    def testGoodPatchRequests(self):
        
        self.conn.request('PATCH', 'A/50/2014-04-20T12:00:00Z/50/50/123', 'PACTION1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        
        self.conn.request('PATCH', 'A/50/2015-05-20T12:00:00Z/50/51/123', 'PACTION2')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('PATCH', 'C/49/2015-04-23T12:00:00Z/house2/bedroom/light1', 'CACTION1')        
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('PATCH', 'C/user/2014-04-20T12:00:00Z/house1010/atrium/light1', 'CACTION2')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'AL/50/2010-06-20T12:00:00Z/2014-06-20T12:00:00Z/50/50')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), 'PACTION1')

        self.conn.request('GET', 'AL/50/2010-06-20T12:00:00Z/2016-06-20T12:00:00Z/50/50')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), 'PACTION1PACTION2')

    
    def testBadPatchRequests(self):
        self.conn.request('PATCH', 'some/bogus/path')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)
        
        self.conn.request('PATCH', 'A/notenoughtokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('PATCH', 'A/too/many/tokens/are/in/this/request/really')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

    def testGoodDeleteRequests(self):
        self.conn.request('DELETE', 'A/user')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('DELETE', 'D/houseid/ver/room/device')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('DELETE', 'R/houseid/ver/room')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('DELETE', 'H/houseid')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('DELETE', 'U/userid')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

    def testBadDeleteRequests(self):
        self.conn.request('DELETE', 'some/bogus/path')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('DELETE', 'R/notenoughtokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('DELETE', 'H/too/many/tokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

if __name__ == '__main__':
    unittest.main()
