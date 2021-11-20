﻿using System;
using System.Linq;

namespace AdventOfCode.Utilities
{
    public class ReadInput
    {
        public static int[] GetInts(string filename)
        {
            string[] lines = System.IO.File.ReadAllLines(filename);
            return lines.Select(l => Convert.ToInt32(l)).ToArray();
        }

        public static int[] GetIntsFromSingleLine(string inputLine)
        {
            return inputLine.Split(',').Select(l => Convert.ToInt32(l)).ToArray();
        }

        public static long[] GetLongsFromSingleLine(string inputLine)
        {
            return inputLine.Split(',').Select(l => Convert.ToInt64(l)).ToArray();
        }

        public static char[,] GetChars(string filename)
        {
            string[] lines = System.IO.File.ReadAllLines(filename);
            var inputs = lines.Select(l => l.ToCharArray()).ToArray();

            char[,] charArray = new char[lines.Length, lines[0].Length];

            for (int x = 0; x < lines.Length; x++)
            {
                for (int y = 0; y < lines[0].Length; y++)
                {
                    charArray[x, y] = inputs[x][y];
                }
            }

            return charArray;
        }

        public static long[] GetLongs(string filename)
        {
            string[] lines = System.IO.File.ReadAllLines(filename);
            return lines.Select(l => Convert.ToInt64(l)).ToArray();
        }

        public static string[] GetStrings(string filename)
        {
            return System.IO.File.ReadAllLines(filename);
        }
    }
}
