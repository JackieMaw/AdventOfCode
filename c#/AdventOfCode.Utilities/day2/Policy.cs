using System;

namespace day2
{
    internal class Policy
    {
        private int minNumberOfOccurances;
        private int maxNumberOfOccurances;
        private char compulsaryCharacter;

        public Policy(string policyString)
        {
            //1-3 a
            var policyParts = policyString.Split(' ');
                                                                                                                                 
            var numberOfOccurances = policyParts[0].Split('-');
            minNumberOfOccurances = Convert.ToInt32(numberOfOccurances[0]);
            maxNumberOfOccurances = Convert.ToInt32(numberOfOccurances[1]);

            compulsaryCharacter = policyParts[1][0];
        }

        internal bool IsValid(string s)
        {
            //part1
            //int numOccurances = 0;
            //foreach (var c in s)
            //{
            //    if (c.Equals(compulsaryCharacter))
            //        numOccurances++;
            //}
            //return (numOccurances >= minNumberOfOccurances) && (numOccurances <= maxNumberOfOccurances);

            //part2
            int numOccurances = 0;
            foreach (var c in s)
            {
                if (c.Equals(compulsaryCharacter))
                    numOccurances++;
            }

            bool check1 = isCharacter(s, minNumberOfOccurances - 1);
            bool check2 = isCharacter(s, maxNumberOfOccurances - 1);
            return check1 ^ check2;
        }

        private bool isCharacter(string s, int i)
        {
            try
            {
                return s[i].Equals(compulsaryCharacter);
            }
            catch (Exception)
            {
                return false;
            }

        }
    }
}