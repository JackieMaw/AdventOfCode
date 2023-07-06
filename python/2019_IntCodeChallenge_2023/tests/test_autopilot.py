from model.autopilot.room import Room
from model.autopilot.room_info import RoomInfo

ROOM_DESCRIPTION_HULL_BREACH = """


== Hull Breach ==
You got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.

Doors here lead:
- north
- south
- west

Command?
"""

ROOM_DESCRIPTION_HALLWAY = """


== Hallway ==
This area has been optimized for something; you're just not quite sure what.

Doors here lead:
- north
- east
- south

Items here:
- mouse

Command?
"""


def test_room_parsing_hull_breach():

    room_info = RoomInfo(ROOM_DESCRIPTION_HULL_BREACH)

    assert room_info.name == "Hull Breach"
    assert room_info.doors == ["north", "south", "west"]
    assert room_info.items == []

def test_room_parsing_hallway():

    room_info = RoomInfo(ROOM_DESCRIPTION_HALLWAY)

    assert room_info.name == "Hallway"
    assert room_info.doors == ["north", "east", "south"]
    assert room_info.items == ["mouse"]


def test_get_commands():
    
    room_info = RoomInfo(ROOM_DESCRIPTION_HALLWAY) #this should create a room manually, it should not rely on the text parser

    room = Room(room_info)

    assert room.get_next_commands() == ['take mouse', 'north']