using System;

namespace Day8
{
    internal class Computer
    {
        public Computer()
        {
        }

        public long Accumulator { get; private set; }

        internal void RunProgram(ProgramInstructions program)
        {
            while (true)
            {
                var instruction = program.GetNextInstruction();

                if (instruction == null)
                {
                    return; //program finished
                }

                ProcessInstruction(instruction, program);
            }
        }

        private void ProcessInstruction(string instruction, ProgramInstructions program)
        {
            var instructionParts = instruction.Split(" ");
            var op = instructionParts[0];
            var val = Convert.ToInt32(instructionParts[1]);

            switch (op)
            {
                case "acc": Accumulate(val);
                    break;

                case "jmp": program.Jump(val);
                    break;

                default: //nop
                    break;
            }

        }

        private void Accumulate(int val)
        {
            Accumulator += val;

            //Console.WriteLine($"Accumulate {val} ==> {Accumulator}");
        }
    }
}