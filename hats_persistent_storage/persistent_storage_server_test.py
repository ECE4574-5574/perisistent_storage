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
        removed = """
        print "Starting!"
        self.user = "mysql"
        self.password = ""
        self.database = "test_database"
        #Because unittest seems to run some tests in parallel, we allow the OS to assign us aon open port.
        self.server = pss.HATSPersistentStorageServer(('',0),
            pss.HATSPersistentStorageRequestHandler, self.user, self.password, self.database)
        self.port = self.server.socket.getsockname()[1]
        self.thread = pss.serveInBackground(self.server)
        self.conn = httplib.HTTPConnection('localhost', self.port)
        """


        # Reset the tables for each test!
        removed = """
        sql = inter.MySQLInterface("mysql", "", "test_database")
        sql.reset_tables()
        sql._cnx.commit()
        sql._cur.close()
        sql._cnx.close()
        """


    def setUp(self):
        print "new test!"
        #removed = """
        self.user = "mysql"
        self.password = ""
        self.database = "test_database"
        #Because unittest seems to run some tests in parallel, we allow the OS to assign us aon open port.
        self.server = pss.HATSPersistentStorageServer(('',0),
            pss.HATSPersistentStorageRequestHandler, self.user, self.password, self.database)
        self.port = self.server.socket.getsockname()[1]
        self.thread = pss.serveInBackground(self.server)
        self.conn = httplib.HTTPConnection('localhost', self.port)
        #"""


    def testEmptyQueries(self):
        removed = """
        self.conn.request("POST", "RESET")
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()
        self.conn.request('GET', 'BH/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        resp.read()
        """

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

            disabled = """
            self.conn.request('DELETE', 'H/' + house1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            
            self.conn.request('GET', 'BH/' + house1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 400)
            """
            

    # API calls for DEVICE
    def testDayInLifeQueries2(self):
         
            self.conn.request('POST', 'H', 'House1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            house1_id = resp.read()  


            self.conn.request('POST', 'R/'+ house1_id, 'Room1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            Room1_id = resp.read()

            self.conn.request('GET', 'HD/' + house1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), '[]')

            self.conn.request('GET', 'RD/' + house1_id + '/' + Room1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), '[]')

            self.conn.request('POST', 'D/' + house1_id + '/' + Room1_id + '/' + 'Device1', 'Light1')
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            Light1_id = resp.read()

            self.conn.request('GET', 'DD/' + house1_id + '/' + Room1_id + '/' + Light1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), 'Light1')
           
            removed = """
            self.conn.request('DELETE', 'D/' + house1_id + '/' + Room1_id + '/' + Light1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)

            self.conn.request('GET', 'DD/' + house1_id + '/' + Room1_id + '/' + Light1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 400)
            """

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

            removed = """
            self.conn.request('DELETE', 'R/' + house1_id + '/' + Room1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 200)

            self.conn.request('GET', 'BR/' + house1_id + '/' + Room1_id)
            resp = self.conn.getresponse()
            self.assertEqual(resp.status, 400)
            """
    def testDayInLifeQueries4(self):

        self.conn.request('POST', 'U', 'USERDATA1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        user1_id = resp.read()
       
        self.conn.request('POST', 'UU/' + user1_id, 'NEWDATA')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        resp.read()

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
        removed = """
        self.conn.request('GET', 'BU/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        """

        self.conn.request('POST', 'U', 'USER2036')
        resp = self.conn.getresponse()
        
        user_id = resp.read()

        self.conn.request('GET', 'BU/' + user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.read(), 'USER2036') 

        removed = """
        self.conn.request('DELETE', 'A/' + user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'BU/' + user_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        """


    def testGoodGetHouseQuery(self):
        removed = """
        self.conn.request('GET', 'BH/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        """
        
        self.conn.request('POST', 'H', 'house47')
        resp = self.conn.getresponse()
        house47_id = resp.read()
       
        self.conn.request('GET', 'BH/' + house47_id)
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        self.assertEqual(resp.read(), 'house47')

#self.conn.request('GET', 'BH/1/address')
#resp = self.conn.getresponse()
#self.assertEqual(resp.status, 200)

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
        removed = """
        self.conn.request('PATCH', 'A/user2002/timestamp/house201')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('PATCH', 'A/user2002/timestamp/house201/hvac')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('PATCH', 'A/user2002/timestamp/house201/light1/atrium')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('PATCH', 'C/user/timestamp/house59')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('PATCH', 'C/user/timestamp/house40/hvac')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        
        self.conn.request('PATCH', 'C/user/timestamp/house1010/light1/atrium')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        """

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

        removed = """
    def testGoodDeleteRequests(self):
        self.conn.request('DELETE', 'A/user')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('DELETE', 'D/houseid/ver/room/device')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('DELETE', 'R/houseid/ver/room')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('DELETE', 'H/houseid')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('DELETE', 'U/userid')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

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
        """

    def tearDown(self):
        self.server.shouldStop = True
        self.thread.join(5)

if __name__ == '__main__':
    unittest.main()
