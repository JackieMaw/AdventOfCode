using System;
using System.Collections.Generic;
using System.Linq;

namespace Day14
{
    internal class Computer2
    {
        public Computer2()
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

            var memoryIndices = ApplyBitMask(memoryIndex);

            string memoryAddressesToPrint = string.Join(", ", memoryIndices.Select(i => i.ToString()));
            Console.WriteLine($"WriteToMemory: {numberToWrite} @ {memoryIndices.Count()} addresses: ({memoryAddressesToPrint})");

            foreach (var actualMemoryIndex in memoryIndices)
            {
                Memory[actualMemoryIndex] = numberToWrite;
            }
        }

        private IEnumerable<long> ApplyBitMask(long memoryIndex)
        {
            int[] binary = ExpandToBinary(memoryIndex);

            IEnumerable<int[]> newBinaries = ApplyBitMaskBinary(binary, BitMask);

            return newBinaries.Select(b => CompressToLong(b));
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
        private IEnumerable<int[]> ApplyBitMaskBinary(int[] binary, char[] bitMask)
        {
            int[] newBinary = new int[36];
            for (int i = 0; i < binary.Length; i++)
            {
                switch (bitMask[i])
                {
                    case '0': //do nothing
                        newBinary[i] = binary[i];
                        break;
                    case '1':
                        newBinary[i] = 1;
                        break;
                    case 'X': //do nothing YET
                        newBinary[i] = binary[i];
                        break;
                    default:
                        throw new Exception($"unsupported bitmask {bitMask[i]}");
                }
            }

            List<int[]> allNewBinaries = new List<int[]> { newBinary };

            for (int i = 0; i < binary.Length; i++)
            {
                switch (bitMask[i])
                {
                    case 'X': //now remove array, modify and add back two
                        List<int[]> temp = new List<int[]>();
                        foreach (var b in allNewBinaries)
                        {
                            var b1 = b.ToArray();
                            b1[i] = 0;
                            var b2 = b.ToArray();
                            b2[i] = 1;
                            temp.Add(b1);
                            temp.Add(b2);
                            allNewBinaries = temp;
                        }
                        break;
                    default:
                        break;
                }
            }

            return allNewBinaries;
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