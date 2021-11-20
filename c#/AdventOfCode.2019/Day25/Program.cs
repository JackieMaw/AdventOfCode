using AdventOfCode.Utilities;
using MyComputer;
using System;

namespace Day25
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Look around the ship and see if you can find the password for the main airlock.");
            Console.WriteLine();

            var program = ReadInput.GetLongsFromSingleLine(ReadInput.GetStrings("Input.txt")[0]);
            using (var bot = new ExplorerBot())
            {
                var answer = new IntCodeComputer(bot).RunProgram(program);
                Console.WriteLine();
                Console.WriteLine($"answer: {answer}");
            }
        }
    }
}
