import unittest
import httplib
import persistent_storage_server as pss
import mysqlinterface as inter

class PersistentStorageServertest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        sql = inter.MySQLInterface("matthew", "password", "test2")
        sql.reset_tables()
        sql._cnx.commit()
        sql._cur.close()
        sql._cnx.close()

    def setUp(self):
        #Because unittest seems to run some tests in parallel, we allow the OS to assign us aon open port.
        self.server = pss.HATSPersistentStorageServer(('',0), pss.HATSPersistentStorageRequestHandler)
        self.port = self.server.socket.getsockname()[1]
        self.thread = pss.serveInBackground(self.server)
        self.conn = httplib.HTTPConnection('localhost', self.port)

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

        self.conn.request('POST', 'U/USER2036', 'USER2036')
        resp = self.conn.getresponse()
        self.assertEqual(resp.read(), 1)

        self.conn.request('GET', 'BU/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.read(), 'USER2036') 

        self.conn.request('GET', 'BU/1/email')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

    def testGoodGetHouseQuery(self):
        self.conn.request('GET', 'BH/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 404)
        
        self.conn.request('POST', 'H/house47', 'house47')
        resp = self.conn.getresponse()
        self.assertEqual(resp.read(), 1)
       
        self.conn.request('GET', 'BH/1')
        resp = self.conn.getresponse()
        self.assertEqual(resp.read(), 'house47')

        self.conn.request('GET', 'BH/1/address')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

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
        self.conn.request('POST', 'D/house2021/15/atrium/light/light20/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('POST', 'R/house2022/15/atrium/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)
        
        self.conn.request('POST', 'H/house2040/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('POST', 'U/someNewUser')
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

        self.conn.request('POST', 'R/notenoughtokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'R/houseID/ver/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'H')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

        self.conn.request('POST', 'U/too/many/tokens')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 400)

    def testGoodPatchRequests(self):
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

    def tearDown(self):
        self.server.shouldStop = True
        self.thread.join(5)

if __name__ == '__main__':
    unittest.main()
