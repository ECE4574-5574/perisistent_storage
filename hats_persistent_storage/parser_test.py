import unittest
import parser
import datetime

class ParserTest(unittest.TestCase):
  def setUp(self):
    pass
  def testPositiveRequestValidations(self):
    self.assertTrue(parser.validateGetRequest("HD/house4/"))
    self.assertTrue(parser.validatePostRequest("H/house224/"))
    self.assertTrue(parser.validatePatchRequest("A/user1/timestamp/house201"))
    self.assertTrue(parser.validateDeleteRequest("A/user/"))

  def testNegativeRequestValidations(self):
    self.assertFalse(parser.validateGetRequest("Z/house4/"))
    self.assertFalse(parser.validatePostRequest("Z/house224/"))
    self.assertFalse(parser.validatePatchRequest("Z/user1/timestamp/house201"))
    self.assertFalse(parser.validateDeleteRequest("Z/user/"))

  def testGetGoodInformation(self):
    path = "CT/user40/timestamp/lightbulb/house14/ballroom"
    self.assertEquals(parser.getHouseID(path), "house14")
    self.assertEquals(parser.getUserID(path), "user40")
    self.assertEquals(parser.getRoomID(path), "ballroom")
    self.assertEquals(parser.getDeviceType(path), "lightbulb")

    self.assertEquals(parser.getDeviceID("CI/user10/timestamp/hlight41/house10/ballroom"), "hlight41")
    self.assertEquals(parser.getVersion("D/houseid/ver/room/device"), "ver")
    self.assertEquals(parser.getTimeFrame("AI/user10/Thu, 25 Sep 2003 10:49:41/light41/house10/ballroom"), datetime.datetime(2003, 9, 25, 10, 49, 41))

  def testGetBadInformation(self):
    path = "NOT_A_GOOD_PATH"
    self.assertFalse(parser.getHouseID(path))
    self.assertFalse(parser.getUserID(path))
    self.assertFalse(parser.getRoomID(path))
    self.assertFalse(parser.getDeviceType(path))
    self.assertFalse(parser.getDeviceID(path)) 
    self.assertFalse(parser.getVersion(path))
    self.assertFalse(parser.getTimeFrame(path))

if __name__ == '__main__':
  unittest.main()