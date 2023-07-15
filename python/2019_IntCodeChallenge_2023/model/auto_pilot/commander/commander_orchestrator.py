from model.auto_pilot.commander.commander import Commander
from model.auto_pilot.commander.explorer import Explorer
from model.auto_pilot.commander.juggler import Juggler
from model.auto_pilot.commander.navigator import Navigator


class CommanderOrchestrator(Commander):

    def __init__(self):
        all_rooms = {}
        items = []
        self._all_commanders = [Explorer(all_rooms, items), Navigator(all_rooms, "Hull Breach", "Security Checkpoint"), Juggler(items)]
    
    def get_next_commands(self, room_description):
        while len(self._all_commanders) > 0:
            current_commander = self._all_commanders[0]
            next_commands = current_commander.get_next_commands(room_description)
            if next_commands == [None]:
                self._all_commanders.pop(0)
                print(f"COMMANDER IS COMPLETE: {type(current_commander)}")
            else:
                return next_commands
        return None

