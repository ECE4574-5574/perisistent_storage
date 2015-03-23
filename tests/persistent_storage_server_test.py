import unittest
import httplib
from hats_persistent_storage import persistent_storage_server as pss

class PersistentStorageServertest(unittest.TestCase):
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
        self.conn.request('GET', 'UI/USER2034')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'UI/USER2034/email')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

    def testGoodGetHouseQuery(self):
        self.conn.request('GET', 'HI/house47')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 200)

        self.conn.request('GET', 'HI/house47/address')
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
        self.assertEqual(resp.status, 500)

        self.conn.request('GET', 'HD/house47/extratoken')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 500)

        self.conn.request('GET', 'HD/')
        resp = self.conn.getresponse()
        self.assertEqual(resp.status, 500)

    def tearDown(self):
        self.server.shouldStop = True
        self.thread.join(5)

if __name__ == '__main__':
    unittest.main()
