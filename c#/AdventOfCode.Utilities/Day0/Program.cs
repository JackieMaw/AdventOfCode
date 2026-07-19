using AdventOfCode.Utilities;
using System;

namespace Day0
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What is the answer to the question?");

            long answer = ReadInput.GetStrings(@"C:\Work\AdventOfCode\Data\2020\input\input_2020_0.txt").Length;

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }
    }
}
