using System;
using System.Collections.Generic;
using System.Linq;

namespace Day10
{
    internal class Adapter
    {
        internal readonly int Joltage;
        internal readonly List<Adapter> Children = new List<Adapter>();
        private long numberOfPaths = 0;

        public Adapter(int joltage)
        {
            Joltage = joltage;
        }

        internal long GetNumberOfPaths()
        {
            if (numberOfPaths > 0)
                return numberOfPaths;

            if (Children.Any())
            {
                numberOfPaths = Children.Select(c => c.GetNumberOfPaths()).Sum();
            } 
            else
            {
                numberOfPaths = 1;
            }

            return numberOfPaths;
        }
    }
}