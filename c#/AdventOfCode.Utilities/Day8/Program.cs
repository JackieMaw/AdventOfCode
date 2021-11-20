using AdventOfCode.Utilities;
using System;

namespace Day8
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Immediately before any instruction is executed a second time, what value is in the accumulator?");

            long answer = GetValueInAccumulatorBeforeInfiniteLoop(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?");

            answer = GetValueInAccumulatorAfterRemovingInfiniteLoop(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetValueInAccumulatorBeforeInfiniteLoop(string [] instructions)
        {
            var program = new ProgramInstructions(instructions);

            var computer = new Computer();

            try
            {
                computer.RunProgram(program);
            }
            catch (InfiniteLoopDetectedException)
            {
                Console.WriteLine("InfiniteLoopDetectedException");
            }

            return computer.Accumulator;
        }
        private static long GetValueInAccumulatorAfterRemovingInfiniteLoop(string[] instructions)
        {
            int instructionFlipped = -1;

            while (true)
            {
                var program = new ProgramInstructions(instructions);
                instructionFlipped = program.FlipNextInstruction(instructionFlipped);

                Console.WriteLine($"Attempting to flip instruction {instructionFlipped}");
                var computer = new Computer();

                try
                {
                    computer.RunProgram(program);
                    return computer.Accumulator;
                }
                catch (InfiniteLoopDetectedException)
                {
                    Console.WriteLine("InfiniteLoopDetectedException");
                }


            } //missing edge case, if we never find a solution
        }
    }
}
