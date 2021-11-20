using System;

namespace Day8
{
    internal class ProgramInstructions
    {
        private string[] instructions;
        private bool[] instructionsVisited;
        int instructionCounter = 0;
        int flipMe = -1;
        private int maxInstruction;

        public ProgramInstructions(string[] instructions)
        {
            this.instructions = instructions;
            maxInstruction = instructions.Length;
            instructionsVisited = new bool[maxInstruction];
        }

        public int FlipNextInstruction(int lastInstructionFlipped)
        {
            int ic = lastInstructionFlipped + 1;
            while (true)
            {
                if (instructions[ic].StartsWith("jmp") || instructions[ic].StartsWith("nop"))
                {
                    flipMe = ic;
                    return flipMe;
                }
                ic++;
            } //missing edge case when we run out of instructions
        }

        public string GetNextInstruction()
        {
            if (instructionCounter >= maxInstruction)
                return null; //program done

            if (instructionsVisited[instructionCounter] == true)
                throw new InfiniteLoopDetectedException();

            var instruction = instructions[instructionCounter];
            //Console.WriteLine($"GetNextInstruction {instructionCounter} ==> {instruction}");

            if (instructionCounter == flipMe)
            {
                instruction = FlipMe(instruction);
            }

            instructionsVisited[instructionCounter] = true;
            instructionCounter++;

            return instruction;
        }

        private string FlipMe(string instruction)
        {
            Console.WriteLine($"You've been Flipped {instructionCounter} ==> {instruction}");

            if (instruction.StartsWith("jmp"))
            {
                return instruction.Replace("jmp", "nop");
            }
            else if (instruction.StartsWith("nop"))
            {
                return instruction.Replace("nop", "jmp");
            }
            return null;
        }

        public void Jump(int i)
        {
            instructionCounter += i - 1;
        }
    }
}