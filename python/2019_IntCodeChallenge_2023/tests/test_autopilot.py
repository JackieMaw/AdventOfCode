from model.auto_pilot.auto_pilot import Explorer
from model.auto_pilot.room import Room
from model.auto_pilot.room_parser import get_room_info

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

ROOM_DESCRIPTION_SECURITY_CHECKPOINT = """


== Security Checkpoint ==
In the next room, a pressure-sensitive floor will verify your identity.

Doors here lead:
- north
- east

Command?
"""

def setup_room(room_description, way_out):
    (name, doors, items)  = get_room_info(room_description)
    return Room(name, doors, items, way_out)

def test_room_parsing_hull_breach():

    room = setup_room(ROOM_DESCRIPTION_HULL_BREACH, None)

    assert room.name == "Hull Breach"
    assert list(room.doors.keys()) == ["north", "south", "west"]
    assert room.items == []

def test_room_parsing_hallway():

    room = setup_room(ROOM_DESCRIPTION_HALLWAY, None)

    assert room.name == "Hallway"
    assert list(room.doors.keys())  == ["north", "east", "south"]
    assert room.items == ["mouse"]


def test_get_commands():
    
    room = setup_room(ROOM_DESCRIPTION_HALLWAY, "south") #this should create a room manually, it should not rely on the text parser

    auto_pilot = Explorer()
    assert auto_pilot._get_next_commands_for_room(room) == ['take mouse', 'north']

def test_get_commands_no_doors_left_must_exit():
    
    room = setup_room(ROOM_DESCRIPTION_HALLWAY, "south") #this should create a room manually, it should not rely on the text parser

    room.connect_room("north", room)
    room.connect_room("south", room)
    room.connect_room("east", room)

    auto_pilot = Explorer()
    assert auto_pilot._get_next_commands_for_room(room) == ['take mouse', 'south']

def test_get_commands_no_doors_left_no_exit():
    
    room = setup_room(ROOM_DESCRIPTION_HULL_BREACH, None) #this should create a room manually, it should not rely on the text parser

    room.connect_room("north", room)
    room.connect_room("south", room)
    room.connect_room("west", room)

    auto_pilot = Explorer()
    assert auto_pilot._get_next_commands_for_room(room) == [None]

def test_get_commands_do_not_pass_security_checkpoint():
    
    room = setup_room(ROOM_DESCRIPTION_SECURITY_CHECKPOINT, "north") #this should create a room manually, it should not rely on the text parser

    auto_pilot = Explorer()
    assert auto_pilot._get_next_commands_for_room(room) == ['north']