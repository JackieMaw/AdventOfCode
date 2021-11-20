using AdventOfCode.Utilities;
using System;
using System.Linq;

namespace Day14b
{
    class Program
    { 
        static void Main(string[] args)
        {
            Console.WriteLine("What is the sum of all values left in memory after it completes?");

            var answer = GetSumOfMemoryValues(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetSumOfMemoryValues(string[] instructions)
        {
            var computer = new Computer();

            foreach (var instruction in instructions)
            {
                computer.ProcessInstruction(instruction);
            }

            return computer.Memory.Values.Sum();
        }
    }
}
}
