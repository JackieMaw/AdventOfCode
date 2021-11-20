using AdventOfCode.Utilities;
using System;

namespace Day12
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What is the Manhattan distance between that location and the ship's starting position?");

            long answer = GetDistance(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetDistance(string[] instructions)
        {
            var myTurtle = new Turtle(10, 1);

            foreach (var i in instructions)
            {
                myTurtle.MoveWaypoint(i);
            }

            return myTurtle.GetDistance();
        }
    }
}
