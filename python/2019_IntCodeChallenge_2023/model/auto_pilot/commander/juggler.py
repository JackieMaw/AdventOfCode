from model.auto_pilot.commander.commander import Commander


class Juggler(Commander):

    def __init__(self, items):
        self._items = items

    def get_next_commands(self, room_description):
        raise NotImplementedError()