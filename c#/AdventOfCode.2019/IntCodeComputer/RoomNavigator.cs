using System;
using System.Collections.Generic;
using System.Linq;

namespace MyComputer
{
    public class RoomNavigator
    {
        private readonly string[] path;
        private int pathStep;

        public RoomNavigator((Room startingRoom, Room targetRoom, Dictionary<string, Room> roomLookup) rooms)
        {
            this.path = GetInstructionPath(rooms.roomLookup, rooms.startingRoom, rooms.targetRoom);
        }

        internal string GetNextInstruction((string room, string[] possibleDirections, string[] items) roomInfo)
        {
            if (pathStep < path.Length)
            {
                return path[pathStep++];
            }
            else
                return null;
        }

        private string[] GetInstructionPath(Dictionary<string, Room> roomLookup, Room startingRoom, Room targetRoom)
        {
            string[] roomNames = roomLookup.Keys.ToArray();
            int numberOfRooms = roomNames.Length;

            //init as 0 = not visited yet
            bool[] visitedYet = new bool[numberOfRooms];
            int?[] allDistances = new int?[numberOfRooms];
            Dictionary<string, (string room, string direction)> shortestPathIsFrom = new Dictionary<string, (string room, string direction)>();

            int startIndex = Array.IndexOf(roomNames, startingRoom.RoomName);
            allDistances[startIndex] = 0;
            shortestPathIsFrom[startingRoom.RoomName] = (startingRoom.RoomName, null);

            Visit(startIndex, roomNames, visitedYet, allDistances, shortestPathIsFrom, roomLookup);

            return GetPathTo(shortestPathIsFrom, targetRoom.RoomName);
        }

        private string[] GetPathTo(Dictionary<string, (string room, string direction)> shortestPathIsFrom, string roomName)
        {
            Stack<string> directions = new Stack<string>();

            while(shortestPathIsFrom.ContainsKey(roomName))
            {
                (var previousRoom, var direction) = shortestPathIsFrom[roomName];

                if (roomName == previousRoom)
                    return directions.ToArray();

                roomName = previousRoom;
                directions.Push(direction);
            }

            return null;
        }

        private static void Visit(int currentIndex, string[] roomNames, bool[] visitedYet, int?[] allDistances, Dictionary<string, (string room, string direction)> shortestPathIsFrom, Dictionary<string, Room> roomLookup)
        {
            string roomName = roomNames[currentIndex];
            var room = roomLookup[roomName];

            if (visitedYet[currentIndex])
            {
                Console.WriteLine($"Skipping #{currentIndex} {roomName}... ALREADY VISITED!");
                return;
            }

            Console.WriteLine($"Beginning Round for #{currentIndex} {roomName}...");

            visitedYet[currentIndex] = true;

            foreach (var pair in room.Directions)
            {
                var direction = pair.Key;
                var nextRoom = pair.Value;
                int nextRoomIndex = Array.IndexOf(roomNames, nextRoom.RoomName);

                int? currentTotalDistance = allDistances[nextRoomIndex];
                int newTotalDistance = allDistances[currentIndex].Value + 1;

                if (!currentTotalDistance.HasValue || (newTotalDistance < currentTotalDistance.Value))
                {
                    allDistances[nextRoomIndex] = newTotalDistance;
                    shortestPathIsFrom[nextRoom.RoomName] = (room.RoomName, direction);
                    Console.WriteLine($"Shortest Distance to #{nextRoom.RoomName} found via #{currentIndex} {roomName} {direction} = {newTotalDistance}");
                }

                Visit(nextRoomIndex, roomNames, visitedYet, allDistances, shortestPathIsFrom, roomLookup);
            }

        }
    }
}