import heapq
from model.auto_pilot.commander.commander import Commander

class Navigator(Commander): 
   
    def __init__(self, all_rooms, start_room, end_room):
        self._all_rooms = all_rooms
        self._start_room = start_room
        self._end_room = end_room

    def get_next_commands(self, room_description):

        start = self._all_rooms[self._start_room]
        end = self._all_rooms[self._end_room]

        shortest_path = self._get_shortest_path(start, end)

        return shortest_path
    
    def _get_shortest_path(self, start_room, end_room):

        shortest_path = {}
        visited_rooms = []

        # technically no need for priority queue because graph is unweighted
        # this is the same as as breadth-first search, which you could use a normal queue for
        priority_queue = [(0, start_room)]
        shortest_path[start_room.name] = (0, None, None)

        while len(priority_queue) > 0:
            (distance_to_current_room, current_room) = heapq.heappop(priority_queue)
            visited_rooms += current_room.name
            
            for (door, neighbouring_room) in current_room.doors.items():
                if neighbouring_room.name not in visited_rooms:  
                    new_distance_to_neighbouring_room = distance_to_current_room + 1

                    if neighbouring_room.name not in shortest_path:
                        shortest_path[neighbouring_room.name] = (new_distance_to_neighbouring_room, current_room, door)
                    
                    else:
                        (old_distance_to_neighbouring_room, old_previous_room, old_direction_from_previous_room) = shortest_path[neighbouring_room.name]

                        if new_distance_to_neighbouring_room < old_distance_to_neighbouring_room:
                            shortest_path[neighbouring_room.name] = (new_distance_to_neighbouring_room, current_room, door)

                    if not neighbouring_room.name in visited_rooms:
                        heapq.heappush(priority_queue, (new_distance_to_neighbouring_room, neighbouring_room))

        print("SHORTEST PATH")
        print(shortest_path)

        current_node = end_room
        path = []

        while current_node is not start_room:
             (distance, previous_room, direction_from_previous_room) = shortest_path[current_node.name]
             path.append(direction_from_previous_room)
             current_node = previous_room

        return path.reverse()                          