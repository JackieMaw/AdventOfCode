using System;
using System.Collections.Generic;
using System.Linq;

namespace day16
{
    internal class TicketRule
    {
        public string Fieldname;
        private int min1;
        private int max1;
        private int min2;
        private int max2;

        public IEnumerable<int> ValidRange;

        public TicketRule(string s)
        {
            //departure location: 30-260 or 284-950
            var parts = s.Split(": ");
            Fieldname = parts[0];

            var parts2 = parts[1].Split(" or ");

            var parts2a = parts2[0].Split("-");
            min1 = Convert.ToInt32(parts2a[0]);
            max1 = Convert.ToInt32(parts2a[1]);

            var parts2b = parts2[1].Split("-");
            min2 = Convert.ToInt32(parts2b[0]);
            max2 = Convert.ToInt32(parts2b[1]);

            ValidRange = GetValidRange();//new Lazy<IEnumerable<int>>(GetValidRange);
        }

        private IEnumerable<int> GetValidRange()
        {
            var range = Enumerable.Range(min1, max1 - min1 + 1).Union(Enumerable.Range(min2, max2 - min2 + 1));
            Console.WriteLine($"{Fieldname} has {range.Count()} valid values from ({min1}, {max1}) and ({min2}, {max2})");
            return range;
        }
    }
}