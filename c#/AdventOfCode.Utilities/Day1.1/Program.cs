using AdventOfCode.Utilities;
using System;
using System.Diagnostics;

namespace Day1
{
    class Program
    {
        static readonly int sum = 2020;
        static void Main(string[] args)
        {
            var inputs = ReadInput.GetInts("Input.txt");

            Console.WriteLine("Find the two entries that sum to 2020; what do you get if you multiply them together?");

            PartOne(inputs);

            Console.WriteLine("Find the THREE entries that sum to 2020; what do you get if you multiply them together?");
            
            PartTwo_Option1(inputs);

            PartTwo_Option2(inputs);

            Console.WriteLine("All Done!");
        }

        private static void PartTwo_Option2(int[] inputs)
        {
            //part two - three number sum = O(n2logn) - must sort first!
            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();
            Array.Sort(inputs);
            bool found = false;
            int i = 0;
            while (!found && i < inputs.Length - 2)
            {
                int lptr = i + 1;
                int rptr = inputs.Length - 1;

                while (!found && (rptr > lptr))
                {
                    int remainder = sum - inputs[i];
                    int actualRemainder = inputs[lptr] + inputs[rptr];

                    if (actualRemainder == remainder) //all done! we can stop now
                    {
                        int product = inputs[i] * inputs[lptr] * inputs[rptr];
                        Console.WriteLine($"i={i} {inputs[i]} lptr={lptr} {inputs[lptr]} rptr={rptr} {inputs[rptr]}, sum = {sum}, product = {product}");
                        found = true;
                    }
                    else if (actualRemainder < remainder) //we want the number to get bigger, we must move up
                    {
                        lptr++;
                    }
                    else if (actualRemainder > remainder) //we want the number to get smaller, we must move down
                    {
                        rptr--;
                    }
                }
                i++;
            }
            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");
        }

        private static void PartTwo_Option1(int[] inputs)
        {
            //part two - three number sum = O(n3)
            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();
            for (int i = 0; i < inputs.Length - 2; i++)
            {
                for (int j = i + 1; j < inputs.Length - 1; j++)
                {
                    for (int k = j + 1; k < inputs.Length; k++)
                    {
                        if (inputs[i] + inputs[j] + inputs[k] == sum)
                        {
                            int product = inputs[i] * inputs[j] * inputs[k];
                            Console.WriteLine($"i={i} {inputs[i]} j={j} {inputs[j]} k={k} {inputs[k]}, sum = {sum}, product = {product}");
                        }
                    }
                }
            }
            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");
        }

        private static void PartOne(int[] inputs)
        {
            //part one - two number sum = O(n2)
            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();

            for (int i = 0; i < inputs.Length - 1; i++)
            {
                for (int j = i + 1; j < inputs.Length; j++)
                {
                    if (inputs[i] + inputs[j] == sum)
                        Console.WriteLine($"i={i} {inputs[i]} j={j} {inputs[j]}, sum = {sum}, product = {inputs[i] * inputs[j]}");
                }
            }
            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");            
        }
    }
}
