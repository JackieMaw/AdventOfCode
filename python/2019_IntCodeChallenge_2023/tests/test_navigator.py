from model.auto_pilot.commander.navigator import Navigator
from model.auto_pilot.room import Room


room_a = Room("A", ["east", "south"], [], None)
room_b = Room("B", ["west", "south"], [], None)
room_c = Room("C", ["north", "east", "south"], [], None)
room_d = Room("D", ["north", "west"], [], None)
room_e = Room("E", ["north"], [], None)

ALL_ROOMS = {
    "A" : room_a,
    "B" : room_b,
    "C" : room_c,
    "D" : room_d,
    "E" : room_e
}

room_a.connect_room("east", room_b)
room_a.connect_room("south", room_c)
room_b.connect_room("south", room_d)
room_c.connect_room("east", room_d)
room_c.connect_room("south", room_e)

def test_navigator_a_to_b():
    navigator = Navigator(ALL_ROOMS, "A", "B")
    commands = navigator.get_next_commands("any room description")
    assert commands == ["east"]

def test_navigator_a_to_e():
    navigator = Navigator(ALL_ROOMS, "A", "E")
    commands = navigator.get_next_commands("any room description")
    assert commands == ["south", "south"]