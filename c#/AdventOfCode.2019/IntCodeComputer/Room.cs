using System.Collections.Generic;

namespace MyComputer
{
    public class Room
    {
        public string RoomName;

        public Dictionary<string, Room> Directions = new Dictionary<string, Room>();

        public Room(string roomName)
        {
            RoomName = roomName;
        }
    }
}