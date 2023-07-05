from model.autopilot.room import Room
from model.autopilot.room_info import RoomInfo

ROOM_DESCRIPTION = """== Hallway ==
This area has been optimized for something; you're just not quite sure what.

Doors here lead:
- north
- east
- south

Items here:
- mouse"""

def test_room_parsing():

    room_info = RoomInfo(ROOM_DESCRIPTION)

    assert room_info.name == "Hallway"
    assert room_info.doors == ["north", "east", "south"]
    assert room_info.items == ["mouse"]


def test_get_commands():
    
    room_info = RoomInfo(ROOM_DESCRIPTION)

    room = Room(room_info)

    assert room.get_next_commands() == ['take mouse', 'north']