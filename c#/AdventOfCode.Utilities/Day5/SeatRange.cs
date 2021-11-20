using System;

namespace Day5
{
    internal class SeatRange
    {
        public int min;
        public int max;

        public SeatRange(int min, int max)
        {
            this.min = min;
            this.max = max;
        }

        internal SeatRange GetSubRange(char c)
        {
            int newLength = (max - min) / 2;

            if (c == 'F' || c == 'L')
            {
                return new SeatRange(min, min + newLength);
            }
            else if (c == 'B' || c == 'R')
            {
                return new SeatRange(min + newLength + 1, max);
            }
            throw new Exception();
        }

        public override string ToString()
        {
            return $"[{min},{max}]";
        }
    }
}