using AdventOfCode.Utilities;
using MyComputer;
using System;
using System.Linq;

namespace Day17
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Run your ASCII program. What is the sum of the alignment parameters for the scaffold intersections?");
            Console.WriteLine();

            var program = ReadInput.GetLongsFromSingleLine(ReadInput.GetStrings("Input.txt")[0]);
            using (var bot = new StupidBot())
            {
                var answer = new IntCodeComputer(bot).RunProgram(program);
                Console.WriteLine();
                Console.WriteLine($"answer: {answer}");
            }

            //var answer = GetAlignmentParameters(ReadInput.GetStrings("Input_Ascii.txt"));

        }

        private static long GetAlignmentParameters(string[] inputStrings)
        {
            long alignment = 0;

            for (int row = 0; row < inputStrings.Length; row++)
            {
                string thisLine = inputStrings[row];
                for (int col = 0; col < thisLine.Length; col++)
                {
                    if (thisLine[col] == 'O')
                    {
                        Console.WriteLine($"Intersection @ ({row},{col})");
                        alignment += row * col;
                    }
                }
            }

            return alignment;
        }
    }
}
