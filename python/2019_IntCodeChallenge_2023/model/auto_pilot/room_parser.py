def get_room_info(room_description):
    name = _get_room(room_description)
    doors = _get_doors(room_description)
    items = _get_items(room_description)
    return (name, doors, items)

def _get_room(room_description):
    startIndex = room_description.find("==") + 3
    endIndex = room_description.rfind("==") - 1
    return room_description[startIndex:endIndex]

def _get_doors(room_description):
    startIndex = room_description.find("Doors here lead:") + 19
    endIndex = room_description.find("\n\n", startIndex)
    substring = room_description[startIndex:endIndex]
    return substring.split("\n- ")

def _get_items(room_description):
    startIndex = room_description.find("Items here:")
    if startIndex > 0:
        startIndex = startIndex + 14
        endIndex = room_description.find("\n\n", startIndex)
        substring = room_description[startIndex:endIndex]
        return substring.split("\n- ")
    else:
        return []