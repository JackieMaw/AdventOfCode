from model.autopilot.room import Room


def test_room_parsing():

    room_description = """== Hallway ==
This area has been optimized for something; you're just not quite sure what.

Doors here lead:
- north
- east
- south

Items here:
- mouse"""

    room = Room(room_description)

    assert room.name == "Hallway"
    assert room.doors == ["north", "east", "south"]
    assert room.items == ["mouse"]
