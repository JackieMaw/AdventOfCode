using System;
using System.Collections.Generic;

namespace Day14b
{
    internal class Computer
    {
        public Computer()
        {
        }

        private char[] BitMask = new char[36];
        public Dictionary<long, long> Memory = new Dictionary<long, long>();

        internal void ProcessInstruction(string instruction)
        {
            //mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
            //mem[8] = 11
            //mem[7] = 101
            //mem[8] = 0

            if (instruction.StartsWith("mask"))
            {
                SaveBitMask(instruction);
            }
            else if (instruction.StartsWith("mem"))
            {
                WriteToMemory(instruction);
            }
            else
            {
                throw new Exception($"unsupported instruction {instruction}");
            }
        }

        private void SaveBitMask(string instruction)
        {
            //mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
            string bitMaskString = instruction.Split("=")[1].Trim();
            BitMask = bitMaskString.ToCharArray();
            Console.WriteLine($"SaveBitMask: {bitMaskString}");
        }

        private void WriteToMemory(string instruction)
        {
            var instructionParts = instruction.Split("=");

            string s = instructionParts[0].Split("[")[1].Trim();
            //mem[8] = 11
            //mem[7] = 101
            //mem[8] = 0

            var memoryIndex = Convert.ToInt64(s.Substring(0, s.Length - 1));
            var numberToWrite = Convert.ToInt64(instructionParts[1].Trim());

            var acutalNumberToWrite = ApplyBitMask(numberToWrite);

            Console.WriteLine($"WriteToMemory: {numberToWrite} => {acutalNumberToWrite} @ {memoryIndex}");

            Memory[memoryIndex] = acutalNumberToWrite;
        }

        private long ApplyBitMask(long numberToWrite)
        {
            int[] binary = ExpandToBinary(numberToWrite);

            int [] newBinary = ApplyBitMaskBinary(binary, BitMask);

            return CompressToLong(newBinary);
        }

        private long CompressToLong(int[] binary)
        {
            long sum = 0;
            for (int i = 0; i < binary.Length; i++)
            {
                if (binary[i] == 1)
                {
                    sum += (long)Math.Round(Math.Pow(2, binary.Length - 1 - i));
                }
            }
            return sum;
        }
        private int[] ApplyBitMaskBinary(int[] binary, char[] bitMask)
        {
            int[] newBinary = new int[36];
            for (int i = 0; i < binary.Length; i++)
            {
                switch (bitMask[i])
                {
                    case '0': 
                        newBinary[i] = 0;
                        break;
                    case '1':
                        newBinary[i] = 1;
                        break;
                    case 'X':
                        newBinary[i] = binary[i];
                        break;
                    default:
                        throw new Exception($"unsupported bitmask {bitMask[i]}");
                }
            }
            return newBinary;
        }

        private int[] ExpandToBinary(long numberToWrite)
        {
            var binary = new int[36];

            int binaryBitValue = 2;
            for (int i = 0; i < binary.Length; i++)
            {
                if (numberToWrite > 0)
                {
                    long remainder = numberToWrite % binaryBitValue;
                    binary[binary.Length - i - 1] = (int)(remainder / (binaryBitValue / 2));
                    numberToWrite -= remainder;
                    binaryBitValue *= 2;
                }
            }

            return binary;
        }
    }
}