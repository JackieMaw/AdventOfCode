using AdventOfCode.Utilities;
using System;
using System.Diagnostics;

namespace Day3
{
    class Program
    {   
        static void Main(string[] args)
        {
            var inputs = ReadInput.GetStrings("Input.txt");

            Console.WriteLine("Part One: Starting at the top-right corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?");

            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();

            PartOne(inputs);

            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");

            Console.WriteLine("Part Two...");

            stopWatch.Start();

            PartTwo(inputs);

            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");

            Console.WriteLine("All Done!");
        }

        private static void PartOne(string[] inputs)
        {
            int maxRight = inputs[0].Length;
            int maxDown = inputs.Length;

            long answer = GetNumberOfTrees(inputs, 3, 1, maxRight, maxDown);

            Console.WriteLine($"answer={answer}");
        }

        private static long GetNumberOfTrees(string[] inputs, int right, int down, int maxRight, int maxDown)
        {
            long numberOfTrees = 0;

            int rowCounter = 0;
            int colCounter = 0;

            while (rowCounter < maxDown)
            {
                var currentBlock = inputs[rowCounter][colCounter];    
                if (currentBlock == '#')
                    numberOfTrees++;

                //move next
                colCounter = colCounter + right;
                if (colCounter >= maxRight)
                    colCounter = colCounter - maxRight;

                rowCounter = rowCounter + down;
            }

            Console.WriteLine($"numberOfTrees={numberOfTrees}");

            return numberOfTrees;
        }

        private static void PartTwo(string[] inputs) //PART 2: 5522401584
        {
            int maxRight = inputs[0].Length;
            int maxDown = inputs.Length;

            long n1 = GetNumberOfTrees(inputs, 1, 1, maxRight, maxDown);
            long n2 = GetNumberOfTrees(inputs, 3, 1, maxRight, maxDown);
            long n3 = GetNumberOfTrees(inputs, 5, 1, maxRight, maxDown);
            long n4 = GetNumberOfTrees(inputs, 7, 1, maxRight, maxDown);
            long n5 = GetNumberOfTrees(inputs, 1, 2, maxRight, maxDown);

            long answer = n1 * n2 * n3 * n4 * n5;
            Console.WriteLine($"answer={answer}");
        }
    }
}
