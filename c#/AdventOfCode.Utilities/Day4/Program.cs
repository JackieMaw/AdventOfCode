using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Diagnostics;

namespace Day4
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("In your batch file, how many passports are valid?");

            CalculateNumberOfValidPassports(ReadInput.GetStrings("Input_Valid.txt"));

            CalculateNumberOfValidPassports(ReadInput.GetStrings("Input_Invalid.txt"));

            CalculateNumberOfValidPassports(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine("All Done!");
        }

        private static void CalculateNumberOfValidPassports(string[] inputs)
        {
            long answer = 0;

            var passports = GetPassports(inputs);

            foreach (var p in passports)
            {
                if (p.IsValid())
                {
                    answer++;
                }
            }

            Console.WriteLine($"answer={answer}");
        }

        private static List<Passport> GetPassports(string[] inputs)
        {
            List<Passport> passports = new List<Passport>();

            string current = "";
            for (int i = 0; i < inputs.Length; i++)
            {
                string thisLine = inputs[i].Trim();
                if (string.IsNullOrEmpty(thisLine))
                {
                    passports.Add(new Passport(current));
                    current = "";
                }
                else
                {
                    current += thisLine + " ";
                }
            }

            passports.Add(new Passport(current));
            current = "";

            return passports;
        }
    }
}
