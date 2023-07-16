import itertools
from model.auto_pilot.commander.commander import Commander


class Juggler(Commander):

    def __init__(self, items):
        self._all_items = items
        self._item_combinations = None

    def get_next_commands(self, room_description):

        if self._passed_the_checkpoint(room_description):
            return [None] # nothing more to do, we have passed the checkpoint :-)
        else:            
            if self._item_combinations is None:
                self._item_combinations = self._get_all_item_combinations()
            elif len(self._item_combinations) == 0:
                return [None] # nothing more to do, there are no more combinations to try :-(
            return self.get_commands_for(self._item_combinations.pop(0))

    def _passed_the_checkpoint(self, room_description):
        return False
    
    def _get_all_item_combinations(self):
        item_combinations = []
        for num_items_to_carry in range(0, len(self._all_items)):
            for items_to_keep in itertools.combinations(self._all_items, num_items_to_carry):
                item_combinations.append(items_to_keep)
        return item_combinations
    
    def get_commands_for(self, items_to_keep):
        commands = []
        items_to_drop = set(self._all_items) - set(items_to_keep)
        for item in items_to_drop:
            commands.append(f"drop {item}")
        for item in items_to_keep:
            commands.append(f"take {item}")
        return commands

