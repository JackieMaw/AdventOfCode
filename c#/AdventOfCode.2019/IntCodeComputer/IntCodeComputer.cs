using System;
using System.Collections.Generic;
using System.Linq;

namespace MyComputer
{
    public class IntCodeComputer
    {
        long instructionPointer;
        long relativeBase;

        Dictionary<long, long> memorySpace = new Dictionary<long, long>();

        private IBot bot;

        public IntCodeComputer(IBot bot)
        {
            this.bot = bot;
        }

        public long RunProgram(long[] program)
        {
            InitializeMemorySpace(program);

            instructionPointer = 0;
            long lastOutput = 0;

            long instruction;
            while (memorySpace.TryGetValue(instructionPointer, out instruction))
            {
                //Console.Write($"{instruction} @ {instructionPointer} | ");

                var opCode = instruction % 100;
                var parameters = instruction / 100;

                switch (opCode)
                {
                    case 99:
                        //Console.WriteLine($"END PROGRAM");
                        return lastOutput;
                        //break;
                    case 1:
                        Add(parameters);
                        break;
                    case 2:
                        Multiply(parameters);
                        break;
                    case 3:
                        Input(parameters);
                        break;
                    case 4:
                        lastOutput = Output(parameters);
                        break;
                    case 5:
                        JumpIfTrue(parameters);
                        break;
                    case 6:
                        JumpIfFalse(parameters);
                        break;
                    case 7:
                        IsLessThan(parameters);
                        break;
                    case 8:
                        IsEquals(parameters);
                        break;
                    case 9:
                        AdjustRelativeBase(parameters);
                        break;
                    default:
                        throw new Exception($"UNSUPPORTED OPERATION: {opCode}");
                }
            }
            return -1;
        }

        private void InitializeMemorySpace(long[] program)
        {
            for (long i = 0; i < program.Length; i++)
            {
                memorySpace[i] = program[i];
            }
        }

        private void AdjustRelativeBase(long parameters)
        {
            //Opcode 9 adjusts the relative base by the value of its only parameter.The relative base increases(or decreases, if the value is negative) by the value of the parameter.

            var m1 = parameters % 10;
            long p1 = GetInputParameter(instructionPointer + 1, m1);

            var result = relativeBase + p1;
            //Console.WriteLine($"Adjust Relative Base {relativeBase} + {p1} = {result}");
            relativeBase = result;

            instructionPointer += 2;
        }

        private void Add(long parameters)
        {
            var m1 = parameters % 10;
            var m2 = parameters % 100 / 10;
            var m3 = parameters % 1000 / 100;

            long p1 = GetInputParameter(instructionPointer + 1, m1);
            long p2 = GetInputParameter(instructionPointer + 2, m2);
            var resultAt = GetPointer(instructionPointer + 3, m3);

            var result = p1 + p2;
            memorySpace[resultAt] = result;
            //Console.WriteLine($"Add {p1} + {p2} = {result} ==> {resultAt}");

            instructionPointer += 4;
        }

        private void Multiply(long parameters)
        {
            var m1 = parameters % 10;
            var m2 = parameters % 100 / 10;
            var m3 = parameters % 1000 / 100;

            long p1 = GetInputParameter(instructionPointer + 1, m1);
            long p2 = GetInputParameter(instructionPointer + 2, m2);
            var resultAt = GetPointer(instructionPointer + 3, m3);

            var result = p1 * p2;
            memorySpace[resultAt] = result;
            //Console.WriteLine($"Multiply {p1} * {p2} = {result} ==> {resultAt}");

            instructionPointer += 4;
        }
        private void Input(long parameters)
        {
            long input = bot.GetNextInput();

            var m1 = parameters % 10;
            var resultAt = GetPointer(instructionPointer + 1, m1);

            memorySpace[resultAt] = input;

            instructionPointer += 2;
        }

        private long Output(long parameters)
        {
            var m1 = parameters % 10;
            long output = GetInputParameter(instructionPointer + 1, m1);

            bot.SaveOutput(output);

            instructionPointer += 2;

            return output;
        }

        private void IsLessThan(long parameters)
        {
           // Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter.Otherwise, it stores 0.

            var m1 = parameters % 10;
            var m2 = parameters % 100 / 10;
            var m3 = parameters % 1000 / 100;

            long p1 = GetInputParameter(instructionPointer + 1, m1);
            long p2 = GetInputParameter(instructionPointer + 2, m2);
            var resultAt = GetPointer(instructionPointer + 3, m3);

            long result = p1 < p2 ? 1: 0;

            //Console.WriteLine($"IsLessThan {p1} < {p2} ==> {result} @ {resultAt}");
            memorySpace[resultAt] = result;

            instructionPointer += 4;
        }

        private void IsEquals(long parameters)
        {
            //Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter.Otherwise, it stores 0.

            var m1 = parameters % 10;
            var m2 = parameters % 100 / 10;
            var m3 = parameters % 1000 / 100;

            long p1 = GetInputParameter(instructionPointer + 1, m1);
            long p2 = GetInputParameter(instructionPointer + 2, m2);
            var resultAt = GetPointer(instructionPointer + 3, m3);

            long result = p1 == p2 ? 1 : 0;

            //Console.WriteLine($"IsEquals {p1} == {p2} ==> {result} @ {resultAt}");
            memorySpace[resultAt] = result;

            instructionPointer += 4;
        }

        private void JumpIfTrue(long parameters)
        {
            //Opcode 5 is jump -if-true: if the first parameter is non - zero, it sets the instruction pointer to the value from the second parameter.Otherwise, it does nothing.

            var m1 = parameters % 10;
            var m2 = parameters % 100 / 10;

            long p1 = GetInputParameter(instructionPointer + 1, m1);
            long p2 = GetInputParameter(instructionPointer + 2, m2);

            if (p1 != 0)
            {
                //Console.WriteLine($"p1 = {p1} so JUMP to ==> {p2}");
                instructionPointer = p2;
            }
            else
            {
                //Console.WriteLine($"p1 = {p1} so NO JUMP");
                instructionPointer += 3;
            }
        }

        private void JumpIfFalse(long parameters)
        {
            //Opcode 6 is jump -if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter.Otherwise, it does nothing.

            var m1 = parameters % 10;
            var m2 = parameters % 100 / 10;

            long p1 = GetInputParameter(instructionPointer + 1, m1);
            long p2 = GetInputParameter(instructionPointer + 2, m2);

            if (p1 == 0)
            {
                //Console.WriteLine($"p1 = {p1} so JUMP to ==> {p2}");
                instructionPointer = p2;
            }
            else
            {
                //Console.WriteLine($"p1 = {p1} so NO JUMP");
                instructionPointer += 3;
            }
        }

        private long GetInputParameter(long pointer, long mode)
        {
            return GetValueFromMemory(GetPointer(pointer, mode));
        }
        private long GetPointer(long pointer, long mode)
        {
            if (mode == 0) //pointer contains the pointer
            {
                return GetValueFromMemory(pointer);
            }
            else if (mode == 1) //pointer IS the pointer
            {
                return pointer;
            }
            else if (mode == 2) //pointer contains the relative pointer
            {
                return GetValueFromMemory(pointer) + relativeBase;
            }

            throw new Exception($"Unsupported Mode: {mode}");
        }

        private long GetValueFromMemory(long pointer)
        {
            //memory beyond the initial program starts with the value 0 and can be read or written like any other memory.
            if (memorySpace.TryGetValue(pointer, out long value))
            {
                return value;
            }
            return 0;
        }
    }
}