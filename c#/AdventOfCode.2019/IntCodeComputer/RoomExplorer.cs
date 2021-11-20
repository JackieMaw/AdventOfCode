using System;
using System.Collections.Generic;
using System.Linq;

namespace MyComputer
{
    public class RoomExplorer : IDisposable
    {
        List<string> badItems = new List<string> { "photons", "escape pod", "infinite loop", "giant electromagnet", "molten lava" };

        Dictionary<(string room, string instruction), string> instructionsPlayed = new Dictionary<(string room, string instruction), string>();

        Dictionary<string, string> directionToExitRoom = new Dictionary<string, string>();

        string previousInstruction;
        string previousRoom;

        //List<string> allPossibleDirections = new List<string> { "north", "south", "east", "west" };

        private readonly System.IO.StreamWriter streamWriter;
        public RoomExplorer()
        {
            streamWriter = System.IO.File.CreateText($"Map_{DateTime.Now.ToString("yyyyMMdd_HHmm")}.txt");
        }

        internal string GetNextInstruction((string room, string[] directions, string[] items) roomInfo)
        {            
            //if this is the first time we are entering this room, save the direction
            if (!directionToExitRoom.ContainsKey(roomInfo.room))
            {
                directionToExitRoom[roomInfo.room] = GetOppositeDirection(previousInstruction);
            }

            instructionsPlayed[(previousRoom, previousInstruction)] = roomInfo.room;
            streamWriter.WriteLine($"{previousRoom} => {previousInstruction} => {roomInfo.room}");
            streamWriter.Flush();

            string nextInstruction = null;

            //PICK UP ALL ITEMS (except bad ones)
            if (roomInfo.items != null)
            {
                foreach (var i in roomInfo.items.Where(i => !instructionsPlayed.ContainsKey((roomInfo.room, $"take {i}"))).Where(i => !badItems.Contains(i)))
                {
                    nextInstruction = $"take {i}";
                    instructionsPlayed[(roomInfo.room, nextInstruction)] = "?";
                    break;
                }
            }

            //TRY ALL DIRECTIONS
            if (nextInstruction == null)
            {
                string exitDir = null;
                directionToExitRoom.TryGetValue(roomInfo.room, out exitDir);

                foreach (var direction in roomInfo.directions.Where(d => !instructionsPlayed.ContainsKey((roomInfo.room, d)) && d != exitDir))
                {
                    nextInstruction = direction;
                    instructionsPlayed[(roomInfo.room, nextInstruction)] = "?";
                    break;
                }

                //ONLY IF ALL OTHER DIRECTIONS EXPLORED, EXIT ROOM
                if (nextInstruction == null)
                    nextInstruction = exitDir;
            }            

            previousInstruction = nextInstruction;
            previousRoom = roomInfo.room;

            return nextInstruction;
        }

        internal string[] GetItems()
        {
            return instructionsPlayed.Where(i => i.Key.instruction != null && i.Key.instruction.StartsWith("take")).Select(i => i.Key.instruction.Replace("take ", "")).ToArray();
        }

        internal (Room startingRoom, Room targetRoom, Dictionary<string, Room> roomLookup) GetRoomMap()
        {

            // =>  => Hull Breach
            //Hull Breach => north => Crew Quarters
            //Crew Quarters => take mug => Crew Quarters

            Dictionary<string, Room> roomLookup = new Dictionary<string, Room>();

            //add all rooms to the lookup
            var directionsPlayed = instructionsPlayed.Where(i => !string.IsNullOrEmpty(i.Key.room) && (!i.Key.instruction.StartsWith("take"))).ToArray();
            foreach (var item in directionsPlayed)
            {
                var source = item.Key.room;
                var destination = item.Value;

                if (string.IsNullOrEmpty(source))
                {
                    roomLookup[destination] = new Room(destination);
                }
                else if (!roomLookup.ContainsKey(source))
                {
                    roomLookup[source] = new Room(source);
                }
            }

            foreach (var item in directionsPlayed)
            {
                var source = item.Key.room;
                var instruction = item.Key.instruction;
                var destination = item.Value;

                var sourceRoom = roomLookup[source];
                var destinationRoom = roomLookup[destination];
                sourceRoom.Directions[instruction] = destinationRoom;
            }

            return (roomLookup["Hull Breach"], roomLookup["Security Checkpoint"], roomLookup);
        }

        private string GetOppositeDirection(string previousDirection)
        {
            switch (previousDirection)
            {
                case "north":
                    return "south";
                case "south":
                    return "north";
                case "east":
                    return "west";
                case "west":
                    return "east";
                default:
                    return null;
            }
        }

        public void Dispose()
        {
            streamWriter.Flush();
            streamWriter.Close();
        }
    }
}