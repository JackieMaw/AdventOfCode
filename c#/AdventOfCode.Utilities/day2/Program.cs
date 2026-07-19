using AdventOfCode.Utilities;
using System;

namespace day2
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("How many passwords are valid according to their policies?");
            var inputs = ReadInput.GetStrings(@"C:\Work\AdventOfCode\Data\2020\input\input_2020_2.txt");

            int numberOfValidPasswords = 0;
            foreach (var input in inputs)
            {
                var inputParts = input.Split(':');
                var policy = new Policy(inputParts[0]);
                var password = inputParts[1].Trim();

                var isValid = policy.IsValid(password);
                if (isValid)
                    numberOfValidPasswords++;
            }

            Console.WriteLine($"numberOfValidPasswords: {numberOfValidPasswords}");

            Console.WriteLine("All Done!");
        }
    }
}
