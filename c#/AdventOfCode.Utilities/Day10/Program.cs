using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day10
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?");

            long answer = GetAnswer(ReadInput.GetInts("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?");

            answer = GetDistinctCombinations(ReadInput.GetInts("Input_Sample.txt"));

            Console.WriteLine($"answer={answer}");

            answer = GetDistinctCombinations(ReadInput.GetInts("Input_Sample2.txt"));

            Console.WriteLine($"answer={answer}");

            answer = GetDistinctCombinations(ReadInput.GetInts("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetAnswer(int [] inputs)
        {
            Array.Sort(inputs);

            int oneJolt = 0;
            int threeJolt = 0;

            int diff = inputs[0];
            if (diff == 1)
                oneJolt++;
            if (diff == 3)
                threeJolt++;

            for (int i = 1; i < inputs.Length; i++)
            {
                diff = inputs[i] - inputs[i - 1];
                if (diff == 1)
                    oneJolt++;
                if (diff == 3)
                    threeJolt++;
            }

            threeJolt++;

            Console.WriteLine($"oneJolt: {oneJolt}");
            Console.WriteLine($"threeJolt: {threeJolt}");

            return oneJolt * threeJolt;
        }

        private static long GetDistinctCombinations(int[] inputs)
        {
            Array.Sort(inputs);
            
            var hashTable = new Dictionary<int, Adapter>();


            //add all
            var root = new Adapter(0);
            hashTable.Add(0, root);

            for (int i = 0; i < inputs.Length; i++)
            {
                int joltage = inputs[i];
                hashTable.Add(joltage, new Adapter(joltage));
            }

            //add children
            foreach (var adapter in hashTable.Values)
            {
                for (int i = 1; i <= 3; i++)
                {
                    int joltage = adapter.Joltage + i;
                    if (hashTable.TryGetValue(joltage, out Adapter childAdapter))
                    {
                        adapter.Children.Add(childAdapter);
                    }
                }
            }

            //depth first traversal

            var numberOfPaths = root.GetNumberOfPaths();

            Console.WriteLine($"numberOfBranches: {numberOfPaths}");

            return numberOfPaths;
        }
    }
}
