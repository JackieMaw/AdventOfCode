import heapq
from model.auto_pilot.commander.commander import Commander


class Navigator(Commander):
    def __init__(self, all_rooms, start_room_name, end_room_name):
        self._all_rooms = all_rooms
        self._start_room_name = start_room_name
        self._end_room_name = end_room_name
        self._navigation_completed = False

    def get_next_commands(self, room_description):

        if self._navigation_completed:
            return [None]

        start_room = self._all_rooms[self._start_room_name]
        end_room = self._all_rooms[self._end_room_name]

        shortest_path = self._get_shortest_path(start_room, end_room)

        self._navigation_completed = True

        return shortest_path

    def _get_shortest_path(self, start_room, end_room):
        shortest_path = {}
        visited_rooms = []
        all_rooms = {start_room.name: start_room, end_room.name: end_room}

        # technically no need for priority queue because graph is unweighted
        # this is the same as as breadth-first search, so you could use a normal queue
        # DjkstrA's Algorithm: always follow the shortest path next, if you find a shorter path to any node update the route
        # you will end up with the shortest paths from the start node to all nodes

        priority_queue = [(0, start_room.name)]  # (cost, room_name)
        shortest_path[start_room.name] = (
            0,
            None,
            None,
        )  # room_name = (cost, previous_room_name, door_to_get_to_room)

        while len(priority_queue) > 0:
            (distance_to_current_room, current_room_name) = heapq.heappop(
                priority_queue
            )  # this pops the next closest node off the queue

            visited_rooms.append(current_room_name)
            current_room = all_rooms[current_room_name]

            for door, neighbouring_room in current_room.doors.items():
                if neighbouring_room is not None and neighbouring_room.name not in visited_rooms:  # we have never visited this room before
                    all_rooms[neighbouring_room.name] = neighbouring_room

                    new_distance_to_neighbouring_room = distance_to_current_room + 1

                    if neighbouring_room.name not in shortest_path:
                        shortest_path[neighbouring_room.name] = (
                            new_distance_to_neighbouring_room,
                            current_room.name,
                            door,
                        )

                    else:  # we already have a way to this room, but maybe the new way is shorter?
                        (
                            old_distance_to_neighbouring_room,
                            old_previous_room,
                            old_direction_from_previous_room,
                        ) = shortest_path[neighbouring_room.name]

                        if (
                            new_distance_to_neighbouring_room
                            < old_distance_to_neighbouring_room
                        ):
                            shortest_path[neighbouring_room.name] = (
                                new_distance_to_neighbouring_room,
                                current_room.name,
                                door,
                            )

                    if not neighbouring_room.name in visited_rooms:
                        heapq.heappush(
                            priority_queue,
                            (new_distance_to_neighbouring_room, neighbouring_room.name),
                        )

        print("SHORTEST PATH")
        print(shortest_path)

        current_room_name = end_room.name
        path = []

        while current_room_name is not start_room.name:
            (
                distance,
                previous_room_name,
                direction_from_previous_room,
            ) = shortest_path[current_room_name]
            path.append(direction_from_previous_room)
            current_room_name = previous_room_name

        path.reverse()

        return path
