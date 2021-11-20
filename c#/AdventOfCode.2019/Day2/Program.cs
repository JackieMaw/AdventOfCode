using AdventOfCode.Utilities;
using MyComputer;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day2
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Test Case 1: 109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99 takes no input and produces a copy of itself as output.");
            Console.WriteLine();
            var program = ReadInput.GetLongsFromSingleLine("109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99");
            var answer = GetFinalOutput(program);
            Console.WriteLine($"answer: {answer}");

            Console.WriteLine("Test Case 2: 1102, 34915192, 34915192, 7, 4, 7, 99, 0 should output a 16 - digit number.");
            Console.WriteLine();
            program = ReadInput.GetLongsFromSingleLine("1102, 34915192, 34915192, 7, 4, 7, 99, 0");
            Console.WriteLine();
            answer = GetFinalOutput(program);
            Console.WriteLine($"answer: {answer}");

            Console.WriteLine("Test Case 3: 104, 1125899906842624, 99 should output the large number in the middle.");
            Console.WriteLine();
            program = ReadInput.GetLongsFromSingleLine("104, 1125899906842624, 99");
            answer = GetFinalOutput(program);
            Console.WriteLine($"answer: {answer}");

            ///////////////////////////////////////////////////////////////////////////////

            Console.WriteLine("What BOOST keycode does it produce?");
            Console.WriteLine();
            program = ReadInput.GetLongsFromSingleLine(ReadInput.GetStrings("Input.txt")[0]);
            answer = GetFinalOutput(program);
            Console.WriteLine($"answer: {answer}");

        }

        //private static int FindNounAndVerb(int[] program)
        //{

        //    for (int noun = 0; noun < 100; noun++)
        //    {
        //        for (int verb = 0; verb < 100; verb++)
        //        {
        //            var thisProgram = (int[])program.Clone();

        //            thisProgram[1] = noun;
        //            thisProgram[2] = verb;

        //            int answer = new IntCodeComputer().RunProgram(thisProgram);
        //            if (answer > 0)
        //                Console.WriteLine($"noun: {noun} verb: {verb} answer: {answer}");

        //            if (answer == 19690720)
        //            {
        //                return 100 * noun + verb;
        //            }
        //        }
        //    }
        //    return -1;
        //}

        private static long GetFinalOutput(long[] program)
        {
            var allOutputs = new IntCodeComputer().RunProgram(program).ToArray();

            Console.WriteLine();
            Console.WriteLine("ALL OUTPUT");
            Console.WriteLine(string.Join(", ", allOutputs.Select(o => o.ToString())));
            Console.WriteLine();

            return allOutputs[allOutputs.Length - 1];
        }
    }
}
