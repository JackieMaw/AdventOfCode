using AdventOfCode.Utilities;
using System;
using System.Linq;

namespace Day5
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What is the highest seat ID on a boarding pass?");

            var inputs = ReadInput.GetStrings("Input.txt");

            //GetHighestSeatId(inputs);

            GetMissingSeatIds(inputs);

            Console.WriteLine("All Done!");
        }
        private static void GetHighestSeatId(string[] inputs)
        {
            int answer = inputs.Select(s => GetSeatId(s)).Max();

            Console.WriteLine($"answer={answer}");
        }
        private static void GetMissingSeatIds(string[] inputs)
        {
            var seatIds = inputs.Select(s => GetSeatId(s)).ToArray();

            Array.Sort(seatIds);

            int lastSeatId = 0;
            foreach (var seatId in seatIds)
            {
                if (seatId > lastSeatId + 1)
                {
                    Console.WriteLine($"missing seat range={lastSeatId + 1} to {seatId - 1}");
                }
                lastSeatId = seatId;
            }

            //Console.WriteLine($"answer={answer}");
        }
        private static int GetSeatId(string input)
        {
            var seatRowRange = new SeatRange(0, 127);

            foreach (var c in input.Substring(0, 7))
            {
                seatRowRange = seatRowRange.GetSubRange(c);
            }

            Console.WriteLine($"seatRowRange={seatRowRange}");

            var seatColRange = new SeatRange(0, 7);

            foreach (var c in input.Substring(7, 3))
            {
                seatColRange = seatColRange.GetSubRange(c);
            }

            Console.WriteLine($"seatColRange={seatColRange}");

            int seatId = seatRowRange.min * 8 + seatColRange.min;
            Console.WriteLine($"seatId={seatId}");

            return seatId;
        }
    }
}
