class Room:
     
    def __init__(self, room_description):
        self.name = self._get_room(room_description)
        self.doors = self._get_doors(room_description)
        self.items = self._get_items(room_description)

    def _get_room(self, room_description):
        startIndex = room_description.find("==") + 3
        endIndex = room_description.rfind("==") - 1
        return room_description[startIndex:endIndex]

    def _get_doors(self, room_description):
        startIndex = room_description.find("Doors here lead:") + 19
        endIndex = room_description.find("\n\n", startIndex)
        substring = room_description[startIndex:endIndex]
        return substring.split("\n- ")

    def _get_items(self, room_description):
        
        startIndex = room_description.find("Items here:") + 14
        if startIndex > 0:
            substring = room_description[startIndex:]
            return substring.split("\n- ")
        else:
            return []