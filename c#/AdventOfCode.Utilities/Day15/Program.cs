using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day15
{
    class Program
    {        
        static void Main(string[] args)
        {
            Console.WriteLine("Given your starting numbers, what will be the 2020th number spoken?");

            var answer = GetNthGuess(ReadInput.GetStrings("Input.txt"), 30000000);

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static object GetNthGuess(string[] inputs, int n)
        {
            Dictionary<int, int> guesses = new Dictionary<int, int>();

            var numbers = inputs[0].Split(",").Select(l => Convert.ToInt32(l)).ToArray();
            for (int i = 1; i <= numbers.Length - 1; i++)
            {
                int thisGuess = numbers[i-1];
                guesses[thisGuess] = i;
                Console.WriteLine($"#{i} ==> {thisGuess}");
            }

            //don't save the last guess yet
            int lastGuess = numbers[numbers.Length - 1];
            int lastGuessPosition = numbers.Length;

            for (int i = numbers.Length + 1; i <= n; i++)
            {
                //If that was the first time the number has been spoken, the current player says 0.
                //Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.

                int thisGuess;
                if (guesses.TryGetValue(lastGuess, out int previousGuessPosition))
                {
                    thisGuess = lastGuessPosition - previousGuessPosition;
                }
                else
                {
                    thisGuess = 0;
                }
                guesses[lastGuess] = lastGuessPosition;
                if (i % 10000 == 0)
                    Console.WriteLine($"#{lastGuessPosition} ==> {lastGuess}");

                lastGuess = thisGuess;
                lastGuessPosition = i;
            }
            return lastGuess;
        }
    }
}
