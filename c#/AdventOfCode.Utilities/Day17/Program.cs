using AdventOfCode.Utilities;
using System;

namespace Day17
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("How many cubes are left in the active state after the sixth cycle?");

            long answer = GetNumberOfActiveCubesAfterNCycles(ReadInput.GetChars(@"C:\Work\AdventOfCode\Data\2020\input\input_2020_17.txt"), 6);

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetNumberOfActiveCubesAfterNCycles(char[,] initialSpace, int numIterations)
        {
            var space = new Space(initialSpace);
            for (int i = 0; i < numIterations; i++)
            {
                space.ChargeMe();
            }
            return space.GetNumberOfActiveCubes();
        }
    }       
}
