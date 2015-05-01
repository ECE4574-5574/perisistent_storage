import mysql.connector
from mysql.connector import errorcode
from structures import *

class MySQLInterface:
  def __init__(self, usr, pwd, dtbs):
    # Store information.
    self._dtbs = dtbs;
    self._usr = usr;
    self._pwd = pwd;

    # Try to connect to the given database.
    self._broken = False;
    try:
      self._cnx =  mysql.connector.connect(
          user=self._usr,
          passwd=self._pwd,
          host='localhost');
    except mysql.connector.Error as err:
      self._broken = True;

      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
      return;

    # Create a cursor for the database.
    self._cur = self._cnx.cursor();
    self._cur.execute("CREATE DATABASE IF NOT EXISTS " + self._dtbs);
    self._cur.execute("USE " + self._dtbs);

    # Create strings for each table name
    self._house_table = "houses";
    self._hr_table = "house_rooms";
    self._hd_table = "house_devices";
    self._rd_table = "room_devices";
    self._user_table = "users";
    self._ua_table = "user_actions";
    self._ca_table = "comp_actions";


  # Commits updated to MySQL and cleanly closes the connections.
  def __del__(self):
    self._cnx.commit()
    self._cur.close()
    self._cnx.close()


  # If the broken flag has been set anywhere, do not execute methods.
  def is_broken(self):
    if self._broken:
      print "Can not use method. Error occurred when Table was opened."
      return True;


  # Write changes to MySQL disk regularly in case of server crash.
  def commit_changes(self):
    self._cnx.commit()


  # If the database was freshly created, this is a necessary step.
  def reset_tables(self):
    if self.is_broken(): return

    # The schema for the tables are hardcoded here, modify if changes desired.
    Tables = {}
    Tables['houses'] = (
      "CREATE TABLE houses ("
      "house_id bigint AUTO_INCREMENT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(house_id) );")

    Tables['house_rooms'] = (
      "CREATE TABLE house_rooms ("
      "house_id bigint, "
      "room_id bigint AUTO_INCREMENT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(room_id) );")

    Tables['house_devices'] = (
      "CREATE TABLE house_devices ("
      "house_id bigint, "
      "device_id bigint AUTO_INCREMENT, "
      "device_type bigint, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(device_id) );")

    Tables['room_devices'] = (
      "CREATE TABLE room_devices ("
      "house_id bigint, "
      "room_id bigint, "
      "device_id bigint AUTO_INCREMENT, "
      "device_type bigint, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(device_id) );")

    Tables['users'] = (
      "CREATE TABLE users ("
      "user_id bigint AUTO_INCREMENT, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(user_id) );")

    Tables['user_actions'] = (
      "CREATE TABLE user_actions ("
      "action_id bigint, "
      "time bigint, "
      "house_id bigint, "
      "room_id bigint, "
      "device_id bigint, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(action_id, time, house_id, device_id) );")

    Tables['comp_actions'] = (
      "CREATE TABLE comp_actions ("
      "action_id bigint, "
      "time bigint, "
      "house_id bigint, "
      "room_id bigint, "
      "device_id bigint, "
      "data MEDIUMBLOB, "
      "PRIMARY KEY(action_id, time, house_id, device_id) );")

    # Actually create these tables.
    for name, ddl in Tables.iteritems():
      try:
        self._cur.execute("DROP TABLE IF EXISTS " + name)
        self._cur.execute(ddl);
      except mysql.connector.Error as err:
        print(err.msg)
        self._broken = True;
        return;


  # Internal. Format an insertion query to the house table.
  def __sql_insert_house(self, house):
    query = '''INSERT INTO %s (data) VALUES ''' % (self._house_table) + \
            ''' (%s)'''
    args = [house._data]
    self._cur.execute(query, args)
    return self._cur.lastrowid


  # Internal. Format an insertion query to the house room table.
  def __sql_insert_house_room(self, room):
    query = '''INSERT INTO %s ''' % (self._hr_table) + \
            '''(house_id, data) VALUES (%s, %s)'''
    args = [room._house_id, room._data]
    self._cur.execute(query, args)
    return self._cur.lastrowid


  # Internal. Format an insertion query to the house device table.
  def __sql_insert_house_device(self, device):
    query = '''INSERT INTO %s ''' % (self._hd_table) + \
            '''(house_id, device_type, data) VALUES (%s, %s, %s)'''
    args = [device._house_id, device._device_type, device._data]
    self._cur.execute(query, args)
    return self._cur.lastrowid



  # Internal. Format an insertion query to the room device table.
  def __sql_insert_room_device(self, device):
    query = '''INSERT INTO %s ''' % (self._rd_table) + \
            '''(house_id, device_type, room_id, data) VALUES (%s, %s, %s, %s)'''
    args = [device._house_id, device._device_type,
            device._room_id, device._data]
    self._cur.execute(query, args)
    return self._cur.lastrowid


  # Internal. Add a user to the SQL database.
  def __sql_insert_user(self, user):
    query = '''INSERT INTO %s ''' % (self._user_table) + \
            '''(data) VALUES (%s)'''
    args = [user._data]
    self._cur.execute(query, args)
    return self._cur.lastrowid

  # Internal. Add a user action to the sql database.
  def __sql_insert_user_action(self, action):
    query = '''INSERT INTO %s VALUES ''' % (self._ua_table) + \
            '''(%s, %s, %s, %s, %s, %s)'''
    args = [action._action_id, action._time, action._house_id, action._room_id, 
            action._device_id, action._data]
    self._cur.execute(query, args)


  # Internal. Add a computer action the sql database.
  def __sql_insert_comp_action(self, action):
    query = '''INSERT INTO %s VALUES ''' % (self._ca_table) + \
            '''(%s, %s, %s, %s, %s, %s)'''
    args = [action._action_id, action._time, action._house_id, action._room_id, 
            action._device_id, action._data]
    self._cur.execute(query, args)


  def __sql_query_action(self, table, action_id, house_id, room_id, device_id,
      start_time, end_time):
    query = '''SELECT * FROM %s ''' % (table) 
    args = []

    first = True
    query = query + '''WHERE '''
    if not action_id is None:
      if not first:
        query = query + '''AND '''
      first = False
      query = query + '''action_id = %s '''
      args.append(action_id)

    if not house_id is None:
      if not first:
        query = query + '''AND '''
      first = False
      query = query + '''house_id = %s '''
      args.append(house_id)

    if not room_id is None:
      if not first:
        query = query + '''AND '''
      first = False
      query = query + '''room_id = %s '''
      args.append(room_id)

    if not device_id is None:
      if not first:
        query = query + '''AND '''
      first = False
      query = query + '''device_id = %s '''
      args.append(device_id)

    if not start_time is None:
      if not first:
        query = query + '''AND '''
      first = False
      query = query + '''time >= %s '''
      args.append(start_time)

    if not end_time is None:
      if not first:
        query = query + '''AND '''
      first = False
      query = query + '''time <= %s '''
      args.append(end_time)

    action_list = []
    self._cur.execute(query, args)
    for a_id, time, h_id, r_id, d_id, data in self._cur.fetchall():
      action_list.append(UserAction(a_id, time, h_id, r_id, d_id, data))

    return action_list


  # Internal. Query for devices in a room.
  # Returns empty list if nothing is found.
  def __sql_query_room_devices(self, house_id, room_id, d_type):
    if (d_type is None):
      query = '''SELECT * FROM %s ''' % (self._rd_table) + \
               '''WHERE house_id = %s AND room_id = %s '''
      args = [house_id, room_id]
    else:
      query = '''SELECT * FROM %s ''' % (self._rd_table) + \
              '''WHERE house_id = %s AND room_id = %s ''' + \
              '''AND device_type = %s'''
      args = [house_id, room_id, d_type]
    
    # extract matching devices from the room device table.
    device_list = []
    self._cur.execute(query, args)
    for h_id, r_id, d_id, d_type, data in self._cur.fetchall():
      device_list.append(Device(h_id, d_id, d_type, data, r_id))
    
    return device_list

  # Internal, query for devices in the house/room device tables.
  # Returns empty list if nothing is found.
  def __sql_query_devices(self, house_id, d_type):

    
    if (d_type is None):
      query1 = '''SELECT * FROM %s ''' % (self._rd_table) + \
               '''WHERE house_id = %s '''
      query2 = '''SELECT * FROM %s ''' % (self._hd_table) + \
               '''WHERE house_id = %s '''
      args = [house_id]
    else:
      query1 = '''SELECT * FROM %s WHERE ''' % (self._rd_table) + \
               '''house_id = %s AND device_type = %s '''
      query2 = '''SELECT * FROM %s WHERE ''' % (self._hd_table) + \
               '''house_id = %s AND device_type = %s '''
      args = [house_id, d_type]

    # Devices can be directly in the house
    device_list = []
    self._cur.execute(query1, args)
    for h_id, r_id, d_id, d_type, data in self._cur.fetchall():
      device_list.append(Device(h_id, d_id, d_type, data, r_id))

    # Or devices can be in rooms in the house.
    self._cur.execute(query2, args)
    for h_id, d_id, d_type, data in self._cur.fetchall():
      device_list.append(Device(h_id, d_id, d_type, data))

    return device_list


  # Retrieve info about a particular house.
  # Returns "None" if the house doesn't exist.
  def __sql_query_house_data(self, house_id):
    query = '''SELECT * FROM %s ''' % (self._house_table) + \
            '''WHERE house_id = %s '''
    args = [house_id,]
    self._cur.execute(query, args)

    # retrieve the results.
    results = self._cur.fetchall()
    if len(results) == 0:
      return None
    if len(results) > 1:
      raise ValueError("SQL Error. Multiple houses of same ID.")
    
    h_id, data = results[0]
    return data


  # Retrieve info about a particular room.
  # Returns "None" if the room doesn't exist.
  def __sql_query_room_data(self, house_id, room_id):
    query = '''SELECT * FROM %s ''' % (self._hr_table) + \
            '''WHERE house_id = %s AND room_id = %s '''
    args = [house_id, room_id]
    self._cur.execute(query, args)

    results = self._cur.fetchall()
    if len(results) == 0:
      return None
    if len(results) > 1:
      raise ValueError("SQL Error. Multiple rooms of same ID in house.")

    h_id, r_id, data = results[0]
    return data


  # Retrieve a particular device's info from the SQL database.
  # Returns "None" if the device doesn't exist.
  def __sql_query_device_data(self, house_id, device_id, room_id):
    if (room_id is None):
      query = '''SELECT * FROM %s ''' % (self._hd_table) + \
              '''WHERE house_id = %s AND device_id = %s '''
      args = [house_id, device_id]
    else:
      query = '''SELECT * FROM %s ''' % (self._rd_table) + \
              '''WHERE house_id = %s AND ''' + \
              '''room_id = %s AND device_id = %s ''' 
      args = [house_id, room_id, device_id]

    # Fetch and check results.
    self._cur.execute(query, args)
    results = self._cur.fetchall()

    if len(results) == 0:
      return None
    if len(results) > 1:
      raise ValueError("SQL Error. Multiple devices of same ID in room/house.")

    # retrieve and return data
    if (room_id is None):
      h_id, d_id, d_type, data = results[0]
    else:
      h_id, r_id, d_id, d_type, data = results[0]
    return data


  # Return user data for a given user id.
  def __sql_query_user_data(self, user_id):
    query = '''SELECT * FROM %s ''' % (self._user_table) + \
            '''WHERE user_id = %s '''
    args = [user_id]

    self._cur.execute(query, args)
    results = self._cur.fetchall()

    if len(results) == 0:
      return None
    if len(results) > 1:
      raise ValueError("SQL Error. Multiple users of same ID.")
    
    user_id, data = results[0]
    return data


  # Update user data for a given user id.
  def __sql_update_user_data(self, user_id, data):
    query = '''UPDATE %s ''' % (self._user_table) + \
            '''SET data=%s WHERE user_id = %s '''
    args = [data, user_id]
    self._cur.execute(query, args)


  # Update house data for a given house id.
  def __sql_update_house_data(self, house_id, data):
    query = '''UPDATE %s ''' % (self._house_table) + \
            '''SET data=%s WHERE house_id = %s '''
    args = [data, house_id]
    self._cur.execute(query, args)


  # Update room data for a given house id and room id.
  def __sql_update_room_data(self, house_id, room_id, data):
    query = '''UPDATE %s ''' % (self._hr_table) + \
            '''SET data=%s WHERE house_id = %s AND room_id=%s'''
    args = [data, house_id, room_id]
    self._cur.execute(query, args)


  # Update device data given device id, house id, (and room id?)
  def __sql_update_device_data(self, house_id, device_id, data, room_id):
    if (room_id is None):
      query = '''UPDATE %s ''' % (self._hd_table) + \
              '''SET data=%s WHERE house_id = %s AND ''' + \
              '''device_id = %s '''
      args = [data, house_id, device_id]
    else:
      query = '''UPDATE %s ''' % (self._rd_table) + \
              '''SET data=%s WHERE house_id = %s AND ''' + \
              '''room_id=%s AND device_id = %s '''
      args = [data, house_id, room_id, device_id]
    self._cur.execute(query, args)


  # Delete a user from the database.
  def __sql_delete_user(self, user_id):
    query = '''DELETE FROM %s ''' % (self._user_table) + \
            '''WHERE user_id = %s '''
    args = [user_id]
    self._cur.execute(query, args)


  # Delete a house and everything in it from the database.
  def __sql_delete_house(self, house_id):
    query1 = '''DELETE FROM %s ''' % (self._house_table) + \
             '''WHERE house_id = %s '''
    query2 = '''DELETE FROM %s ''' % (self._hr_table) + \
             '''WHERE house_id = %s '''
    query3 = '''DELETE FROM %s ''' % (self._hd_table) + \
             '''WHERE house_id = %s '''
    query4 = '''DELETE FROM %s ''' % (self._rd_table) + \
             '''WHERE house_id = %s '''
    args = [house_id]
    self._cur.execute(query1, args)
    self._cur.execute(query2, args)
    self._cur.execute(query3, args)
    self._cur.execute(query4, args)


  # Delete a room and everything in it from the database.
  def __sql_delete_room(self, house_id, room_id):
    query1 = '''DELETE FROM %s ''' % (self._hr_table) + \
             '''WHERE house_id = %s AND room_id = %s '''
    query2 = '''DELETE FROM %s ''' % (self._rd_table)+ \
             '''WHERE house_id = %s AND room_id = %s '''
    args = [house_id, room_id]
    self._cur.execute(query1, args)
    self._cur.execute(query2, args)


  # Delete a particular house device.
  def __sql_delete_hd(self, house_id, device_id):
    query = '''DELETE FROM %s ''' % (self._hd_table) + \
            '''WHERE house_id = %s AND device_id = %s '''
    args = [house_id, device_id]
    self._cur.execute(query, args)


  # Delete a particular room device.
  def __sql_delete_rd(self, house_id, room_id, device_id):
    query = '''DELETE FROM %s ''' % (self._rd_table) + \
            '''WHERE house_id = %s AND ''' + \
            '''room_id = %s AND device_id = %s '''
    args = [house_id, room_id, device_id]
    self._cur.execute(query, args)


  # Insert a house into the SQL database. Calls insert room/device where necessary.
  def insert_house(self, house):
    for room in house._rooms:
      self.insert_room(room)

    for device in house._devices:
      self.insert_house_device(device);

    return self.__sql_insert_house(house)


  # Insert a room into the SQL database. Calls insert device where necessary.
  def insert_room(self, room):
    for device in room._devices:
      self.insert_room_device(device);

    return self.__sql_insert_house_room(room)


  # Insert a device associated with a house but no room.
  def insert_house_device(self, device):
    return self.__sql_insert_house_device(device)


  # Insert a device associated with a room inside of a house.
  # Warning! Make sure room has room ID set.
  def insert_room_device(self, device):
    if (device._room_id == None):
      raise ValueError('SQL: Tried to insert device in room with no room ID')
    return self.__sql_insert_room_device(device)


  # Insert a user into the user table.
  def insert_user(self, user):
    return self.__sql_insert_user(user)


  # Retrieve all devices (of a type?) from a particular house (global and rooms)
  def get_house_devices(self, house_id, d_type=None):
    return self.__sql_query_devices(house_id, d_type)


  # Retrieve all devices (of a type?) from a specific room in a house.
  def get_room_devices(self, house_id, room_id, d_type=None):
    return self.__sql_query_room_devices(house_id, room_id, d_type)


  # Retrieve data about a particular house.
  def get_house_data(self, house_id):
    return self.__sql_query_house_data(house_id)


  # Retrieve data about a particular room.
  def get_room_data(self, house_id, room_id):
    return self.__sql_query_room_data(house_id, room_id)

  # Retrieve data about a particular user.
  def get_user_data(self, user_id):
    return self.__sql_query_user_data(user_id)


  # Retrieve data about a particular device. room_id is required if applicable.
  def get_device_data(self, house_id, device_id, room_id=None):
    return self.__sql_query_device_data(house_id, device_id, room_id)


  # Overwrite the data blob in a user.
  def update_user(self, user_id, newData):
    return self.__sql_update_user_data(user_id, newData)


  # Overwrite the data blob in a house.
  def update_house(self, house_id, newData):
    return self.__sql_update_house_data(house_id, newData)


  # Overwrite the data blob in a room.
  def update_room(self, house_id, room_id, newData):
    return self.__sql_update_room_data(house_id, room_id, newData)


  # Overwrite the data blob in a device.
  def update_device(self, house_id, device_id, newData, room_id=None):
    return self.__sql_update_device_data(house_id, device_id, newData, room_id)


  # Call to delete a particular user.
  def delete_user(self, user_id):
    self.__sql_delete_user(user_id)


  # Call to delete a particular house (and everything inside too!)
  def delete_house(self, house_id):
    self.__sql_delete_house(house_id)


  # Call to delete a particular room (and all devices inside too!)
  def delete_room(self, house_id, room_id):
    self.__sql_delete_room(house_id, room_id)
    return


  # Call to delete a particular device in a room or house.
  def delete_device(self, house_id, device_id, room_id=None):
    if (room_id == 0):
      self.__sql_delete_hd(house_id, device_id)
    else:
      self.__sql_delete_rd(house_id, room_id, device_id)


  # Insert a new user action to the database.
  def insert_user_action(self, action):
    self.__sql_insert_user_action(action)

  # Insert a new computer aciton to the database.
  def insert_comp_action(self, action):
    self.__sql_insert_comp_action(action)


  # Get a list of user actions meeting the given fields. Use "None" if they
  # aren't being included.
  def get_user_actions(self, user_id, house_id, room_id, device_id, start_time,
      end_time):
    return self.__sql_query_action(self._ua_table, user_id, house_id, room_id, device_id,
        start_time, end_time)


  # Get a list of computer actions meeting the given parameters. Use "None" if a
  # parameter isn't being included.
  def get_comp_actions(self, comp_id, house_id, room_id, device_id, start_time,
      end_time):
    return self.__sql_query_action(self._ca_table, comp_id, house_id, room_id, device_id,
        start_time, end_time)
