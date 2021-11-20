using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;

namespace Day7
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("How many bag colors can eventually contain at least one shiny gold bag?");

            long answer = CalculateHowManyBagsCanContain(ReadInput.GetStrings("Input.txt"), "shiny gold");

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("How many bag colors can eventually contain at least one shiny gold bag?");

            answer = CalculateNumberOfBagsAreContainedBy(ReadInput.GetStrings("Input.txt"), "shiny gold");

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long CalculateHowManyBagsCanContain(string [] inputs, string bagColour)
        {
            var allRules =  GetAllRules(inputs);

            long sum = 0;
            foreach (var rule in allRules.Values)
            {
                var number = rule.GetNumberOfBagsWhichCanContain(bagColour);
                if (number > 0)
                    sum++;
            }

            return sum;
        }

        private static long CalculateNumberOfBagsAreContainedBy(string[] inputs, string bagColour)
        {
            var allRules = GetAllRules(inputs);

            var rule = allRules[bagColour];

            return rule.GetNumberOfBags() - 1;
        }
        private static Dictionary<string, Rule> GetAllRules(string[] inputs)
        {
            Dictionary<string, Rule> hashTable = new Dictionary<string, Rule>();

            foreach (var ruleString in inputs)
            {
                var rule = new Rule(ruleString);
                hashTable.Add(rule.Key, rule);
            }

            foreach (var rule in hashTable.Values)
            {
                rule.AddChildRules(hashTable);
            }

            return hashTable;
        }
    }
}
