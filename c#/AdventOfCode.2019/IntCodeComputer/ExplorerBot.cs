using System;
using System.Collections.Generic;
using System.Linq;

namespace MyComputer
{
    public class ExplorerBot : IDisposable, IBot
    {
        Queue<int> inputs = new Queue<int>();

        List<char> outputSinceLastInput = new List<char>();

        private readonly System.IO.StreamWriter streamWriter;

        private readonly RoomExplorer roomExplorer;
        private RoomNavigator roomNavigator;
        private ItemJuggler itemJuggler; 

        string previousRoomText = null;

        string mode = "#explore";

        public ExplorerBot()
        {
            streamWriter = System.IO.File.CreateText($"Input_Output_{DateTime.Now.ToString("yyyyMMdd_HHmm")}.txt");
            roomExplorer = new RoomExplorer();
            
        }
        private List<int> ToAscii(string myString)
        {
            return (myString + "\n").ToCharArray().Select(c => ((int)c)).ToList();
        }

        public long GetNextInput()
        {
            if (!inputs.Any())
            {
                //no recorded input left, ask the user
                GetInputFromUser();
                outputSinceLastInput.Clear();
            }

            var input = inputs.Dequeue();
            streamWriter.Write($"{(char)input}");
            Console.Write($"{(char)input}");
            streamWriter.Flush();

            return input;           
        }

        private void GetInputFromUser()
        {
            streamWriter.Write(">>");
            Console.WriteLine(">>");

            var roomInfo = ParseRoom();

            string instruction = null;
            switch (mode)
            {
                case "#explore":
                    instruction = roomExplorer.GetNextInstruction(roomInfo); 
                    if (instruction == null)
                    {
                        Console.WriteLine("No more instructions from roomExplorer");
                        mode = "#navigate";
                        roomNavigator = new RoomNavigator(roomExplorer.GetRoomMap());
                        instruction = roomNavigator.GetNextInstruction(roomInfo);
                    }
                    break;
                case "#navigate":
                    instruction = instruction = roomNavigator.GetNextInstruction(roomInfo);
                    if (instruction == null)
                    {
                        Console.WriteLine("No more instructions from roomNavigator");
                        mode = "#juggleitems";
                        itemJuggler = new ItemJuggler(roomExplorer.GetItems());
                        instruction = itemJuggler.GetNextInstruction();
                    }
                    break;
                case "#juggleitems":
                    if (PassedTheTest())
                    {
                        mode = "#manual";
                        instruction = null;
                    }
                    else
                    {
                        instruction = instruction = itemJuggler.GetNextInstruction();
                    }
                    break;

                default:
                    break;
            }

            if (instruction == null)
            {
                Console.WriteLine("No more instructions from itemJuggler");
                streamWriter.Write(">>");
                Console.WriteLine(">>");
                instruction = Console.ReadLine();
            }

            ToAscii(instruction).ForEach(i => inputs.Enqueue(i));
        }

        private bool PassedTheTest()
        {
            var roomText = new string(outputSinceLastInput.ToArray());

            if (roomText.Contains("Analyzing..."))
            {
                if (roomText.Contains("Alert! Droids on this ship are lighter"))
                    return false;
                else if (roomText.Contains("Alert! Droids on this ship are heavier"))
                    return false;
                else
                    return true;
            }
            else
            {
                return false;
            }
        }

        private (string room, string[] possibleDirections, string[] items) ParseRoom()
        {
            var roomText = new string(outputSinceLastInput.ToArray());

            if (!roomText.Contains("=="))
            {
                roomText = previousRoomText;
            }
            else
            {
                previousRoomText = roomText;
            }

            var room = ParsetTextToGetRoom(roomText);
            var directions = ParsetTextToGetDirections(roomText);
            var items = ParsetTextToGetItems(roomText);

            return (room, directions, items);
        }

        private static string[] ParsetTextToGetDirections(string text)
        {
            int startIndex = text.LastIndexOf("Doors here lead:");
            int endIndex = text.IndexOf("\n\n", startIndex);
            string substring = text.Substring(startIndex + 17, endIndex - startIndex - 17);
            return substring.Replace("\n", "")
                .Split(new[] { '-' }, StringSplitOptions.RemoveEmptyEntries)
                    .Select(s => s.Trim())
                    .ToArray();
        }

        private static string[] ParsetTextToGetItems(string text)
        {
            int startIndex = text.LastIndexOf("Items here:");

            if (startIndex > 0)
            {
                int endIndex = text.IndexOf("\n\n", startIndex);
                string substring = text.Substring(startIndex + 12, endIndex - startIndex - 12);
                return substring.Replace("\n", "")
                    .Split(new[] { '-' }, StringSplitOptions.RemoveEmptyEntries)
                    .Select(s => s.Trim())
                    .ToArray();
            }
            else
                return null;
        }

        private static string ParsetTextToGetRoom(string text)
        {
            int endIndex = text.LastIndexOf("==");
            int startIndex = text.LastIndexOf("==", endIndex);
            return text.Substring(startIndex + 3, endIndex - startIndex - 4);
        }

        public void Dispose()
        {
            streamWriter.Flush();
            streamWriter.Close();

            roomExplorer.Dispose();
        }
        public void SaveOutput(long output)
        {
            if (output < 128) //ASCII
            {
                Console.Write($"{(char)output}");
                streamWriter.Write($"{(char)output}");

                outputSinceLastInput.Add((char)output);
            }
            else
            {
                Console.Write($"{output}");
                streamWriter.Write($"{output}");


            }
            streamWriter.Flush();
        }
    }
}