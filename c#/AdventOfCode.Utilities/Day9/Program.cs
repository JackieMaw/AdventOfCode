using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;

namespace Day9
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?");

            long answer1 = GetFirstNumberWhichFails(ReadInput.GetLongs("Input.txt"), 25);

            Console.WriteLine($"answer={answer1}");

            Console.WriteLine("you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.");

            Stopwatch stopWatch = new Stopwatch();
            stopWatch.Start();

            long answer = GetMinPlusMax_Slow(ReadInput.GetLongs("Input.txt"), answer1);
            Console.WriteLine($"answer={answer}");

            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");
            stopWatch.Start();

            answer = GetMinPlusMax_Faster(ReadInput.GetLongs("Input.txt"), answer1);
            Console.WriteLine($"answer={answer}");

            stopWatch.Stop();
            Console.WriteLine($"RunTime: {stopWatch.Elapsed.Hours:00}:{stopWatch.Elapsed.Minutes:00}:{stopWatch.Elapsed.Seconds:00}.{stopWatch.Elapsed.Milliseconds:00}");

            Console.WriteLine("All Done!");
        }

        private static long GetFirstNumberWhichFails(long[] inputs, int loopSize)
        {
            //there must be some way to stop recalculating all the sums!!!
            //Queue<Tuple<int, HashSet<int>>> queueOfSums = new Queue<Tuple<int, HashSet<int>>>();
            for (int i = loopSize; i < inputs.Length; i++)
            {
                var allSums = GetAllSums(inputs, i, loopSize);

                var sum = inputs[i];
                if (!allSums.Contains(sum))
                    return sum;
            }

            throw new Exception("All numbers were valid!");
        }

        private static HashSet<long> GetAllSums(long[] inputs, int currentIndex, int loopSize)
        {
            var allSums = new HashSet<long>();

            int startAt = currentIndex - loopSize;
            int endAt = currentIndex - 1;
            //Console.WriteLine($"Calculating sums for {startAt} ==> {endAt}");

            for (int i = startAt; i <= endAt - 1; i++)
            {
                for (int j = i + 1; j <= endAt; j++)
                {
                    allSums.Add(inputs[i] + inputs[j]);
                }
            }

            return allSums;
        }

        public static long GetMinPlusMax_Slow(long[] inputs, long sumSeek) //surely there is a more optimal solution
        {
            long numberOfOperations = 0;

            for (int i = 0; i < inputs.Length - 1; i++)
            {
                for (int j = i + 1; j < inputs.Length; j++)
                {
                    long sum = 0;
                    long min = inputs[i];
                    long max = inputs[i];

                    for (int k = i; k <= j; k++)
                    {
                        numberOfOperations++;

                        long l = inputs[k]; 
                        sum += l;
                        if (l < min)
                            min = l;
                        if (l > max)
                            max = l;
                    }

                    if (sum == sumSeek)
                    {
                        Console.WriteLine($"numberOfOperations: {numberOfOperations}");
                        return min + max;
                    }
                }
            }

            throw new Exception("No Solution Found :-)");
        }

        public static long GetMinPlusMax_Faster(long[] inputs, long sumSeek) //surely there is a more optimal solution
        {
            long numberOfOperations = 0;

            for (int i = 0; i < inputs.Length - 1; i++)
            {
                long sum = 0;
                long min = inputs[i];
                long max = inputs[i];

                for (int j = i; j < inputs.Length; j++)
                {
                    numberOfOperations++;

                    long l = inputs[j];

                    sum += l;
                    if (l < min)
                        min = l;
                    if (l > max)
                        max = l;

                    if (sum == sumSeek)
                    {
                        Console.WriteLine($"numberOfOperations: {numberOfOperations}");
                        return min + max;
                    }
                }
            }

            throw new Exception("No Solution Found :-)");
        }
    }
}
