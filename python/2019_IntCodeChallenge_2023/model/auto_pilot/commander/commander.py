from abc import ABC, abstractmethod


class Commander(ABC):

    @abstractmethod
    def get_next_commands(self, room_description):
        pass