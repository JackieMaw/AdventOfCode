from model.auto_pilot.commander.commander import Commander


class Human(Commander):

    def get_next_commands(self, room_description):
        raise NotImplementedError()