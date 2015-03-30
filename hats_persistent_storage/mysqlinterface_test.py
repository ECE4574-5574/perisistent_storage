import unittest
import httplib
from mysqlinterface import MySQLInterface
from structures import User, House, Room, Device

class MySQLInterfaceTest(unittest.TestCase):
  def setUp(self):
    self.inter = MySQLInterface("matthew", "password", "test_database")
    self.inter.reset_tables()
    self.dev1 = Device("home1", "1", "1", "cat1", "1")
    self.dev2 = Device("home1", "2", "2", "cat2", "1")
    self.dev3 = Device("home1", "3", "1", "dog1", "2")
    self.dev4 = Device("home1", "4", "2", "dog2", "2")
    self.dev5 = Device("home1", "5", "1", "monkey1")
    self.dev6 = Device("home1", "6", "2", "monkey2")

    self.r1devs = [self.dev1, self.dev2]
    self.r2devs = [self.dev3, self.dev4]
    self.h1devs = [self.dev5, self.dev6]

    self.room1 = Room("home1", "1", "cat room", self.r1devs)
    self.room2 = Room("home1", "2", "dog room", self.r2devs)
    self.hrooms = [self.room1, self.room2]

    self.house1 = House("home1", "pet home", self.hrooms, self.h1devs)
    self.house2 = House("home2", "people home", None, None)

    self.user1 = User("1", "OBAMA")
    self.user2 = User("2", "OSAMA")

  def testSanity(self):
    self.assertEqual(1, 1)

  def testInsertionAndQueries(self):
    self.assertEqual(self.inter.get_house_devices("home1", None),
                     [])
    self.inter.insert_house(self.house1)
    self.inter.insert_house(self.house2)
    self.inter.insert_user(self.user1)
    self.inter.insert_user(self.user2)

    # Test data extraction
    self.assertEqual(self.inter.get_house_data(self.house1._house_id),
                     self.house1._data)
    self.assertEqual(self.inter.get_room_data(self.house1._house_id, self.room2._room_id),
                     self.room2._data)
    self.assertEqual(self.inter.get_device_data(self.house1._house_id, self.dev5._device_id),
                     self.dev5._data)
    self.assertEqual(self.inter.get_user_data(self.user1._user_id),
                     self.user1._data)

    # These are requests for items not in the databases.
    self.assertEqual(self.inter.get_house_data("home3"), None)
    self.assertEqual(self.inter.get_room_data(self.house1._house_id, "3"), None)
    self.assertEqual(self.inter.get_device_data(self.house1._house_id, "7"), None)
    self.assertEqual(self.inter.get_user_data("3"), None)
        
    
    # Assert a device query has the proper result.
    answer = [self.dev2, self.dev4, self.dev6]
    result = self.inter.get_house_devices(self.house1._house_id, "2")
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._device_id, result[i]._device_id)

    # Room device query test
    result = self.inter.get_room_devices(self.house1._house_id, self.room2._room_id, None)
    self.assertEqual(len(self.r1devs), len(result))
    for i in range(0, len(result)):
      self.assertEqual(self.r2devs[i]._device_id, result[i]._device_id)

  def testUpdate(self):
    self.inter.insert_house(self.house1)
    self.inter.insert_user(self.user1)

    self.inter.update_house(self.house1._house_id, "ANIMAL HOUSE")
    self.assertEqual(self.inter.get_house_data(self.house1._house_id),
                     "ANIMAL HOUSE")

    self.inter.update_room(self.house1._house_id, self.room1._room_id, "HELLO KITTY ROOM")
    self.assertEqual(self.inter.get_room_data(self.house1._house_id, self.room1._room_id),
                     "HELLO KITTY ROOM")

    self.inter.update_device(self.house1._house_id, self.dev5._device_id, "Curious George")
    self.assertEqual(self.inter.get_device_data(self.house1._house_id, self.dev5._device_id),
                     "Curious George")

    self.inter.update_user(self.user1._user_id, "Mr. President")
    self.assertEqual(self.inter.get_user_data(self.user1._user_id),
                     "Mr. President")

  def testDeletion(self):
    self.inter.insert_house(self.house1)
    self.inter.insert_user(self.user1)

    # Delete device 6
    self.inter.delete_device(self.house1._house_id, self.dev6._device_id)
    self.assertEqual(self.inter.get_device_data(self.house1._house_id, self.dev6._device_id), None)
    
    # Delete device 4
    self.inter.delete_device(self.house1._house_id, self.dev4._device_id, self.room2._room_id)
    answer = [self.dev3]
    result = self.inter.get_room_devices(self.house1._house_id, self.room2._room_id)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._device_id, result[i]._device_id)

    # Delete room 1
    self.inter.delete_room(self.house1._house_id, self.room1._room_id)
    self.assertEqual(self.inter.get_room_data(self.house1._house_id, self.room1._room_id), None)
    answer = [self.dev3, self.dev5]
    result = self.inter.get_house_devices(self.house1._house_id)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._device_id, result[i]._device_id)

    # Delete home 1
    self.inter.delete_house(self.house1._house_id)
    self.assertEqual(self.inter.get_house_data(self.house1._house_id), None)
    answer = []
    result = self.inter.get_house_devices(self.house1._house_id)
    self.assertEqual(len(answer), len(result))
    for i in range(0, len(result)):
      self.assertEqual(answer[i]._device_id, result[i]._device_id)
    

  def tearDown(self):
    del self.inter

if __name__ == '__main__':
  unittest.main()
