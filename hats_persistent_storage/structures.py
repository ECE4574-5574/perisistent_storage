
class Device:
  def __init__(self, device_id, device_type, data):
    self._device_id = device_id
    self._device_type = device_type
    self._data = data

class Room:
  def __init__(self, room_id, data, devices):
    self._room_id = room_id
    self._data = data

    self._devices = []
    for device in devices:
      self._devices.append(device)

class House:
  def __init__(self, house_id, data, rooms, devices):
    self._house_id = house_id
    self._data = data

    self._rooms = []
    for room in rooms:
      self._rooms.append(room)

    self._devices = []
    for device in devices:
      self._devices.append(device)
