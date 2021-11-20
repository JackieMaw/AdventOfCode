using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day6
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What is the sum of those counts?");

            long answer = CalculateSumOfIntersection(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long CalculateSumOfDistinctCount(string[] inputs)
        {
            long totalSum = 0;

            string current = "";
            for (int i = 0; i < inputs.Length; i++)
            {
                string thisLine = inputs[i].Trim();
                if (string.IsNullOrEmpty(thisLine))
                {
                    totalSum += GetDistinctCount(current);
                    current = "";
                }
                else
                {
                    current += thisLine;
                }
            }
            totalSum += GetDistinctCount(current);

            return totalSum;
        }

        private static long GetDistinctCount(string current)
        {
            return current.ToCharArray().Distinct().Count();
        }

        private static long CalculateSumOfIntersection(string[] inputs)
        {
            long totalSum = 0;

            IEnumerable<char> currentIntersection = null; //INITIALISE
            for (int i = 0; i < inputs.Length; i++)
            {
                string thisLine = inputs[i].Trim();
                if (string.IsNullOrEmpty(thisLine))
                {
                    totalSum += currentIntersection.Count(); //PROCESS
                    currentIntersection = null; //INITIALISE
                }
                else
                {
                    if (currentIntersection is null)
                    {
                        currentIntersection = thisLine.ToCharArray(); //BASE CASE
                    }
                    else
                    {
                        currentIntersection = currentIntersection.Intersect(thisLine.ToCharArray()); //ACCUMULATE
                    }
                }
            }
            totalSum += currentIntersection.Count();

            return totalSum;
        }
    }
}
