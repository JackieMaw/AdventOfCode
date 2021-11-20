using System;

namespace Day23
{
    internal class Cup
    {
        public Cup(long cupNumber)
        {
            CupNumber = cupNumber;
        }

        public long CupNumber { get; }
        public Cup NextCup { get; internal set; }

        internal Cup RemoveNextCup()
        {
            Cup removedCup = NextCup;
            NextCup = removedCup.NextCup;
            removedCup.NextCup = null;
            //Console.WriteLine($"Removed Cup: {removedCup.CupNumber}");
            return removedCup;
        }


        internal void InsertCup(Cup cupToInsert)
        {
            Cup nextCup = NextCup;
            NextCup = cupToInsert;
            cupToInsert.NextCup = nextCup;
        }

        public string GetAllCups(int depth = 0)
        {
            if (depth == 20)
                return "";

            return CupNumber + " " + NextCup.GetAllCups(depth + 1);
            
        }

        public override string ToString()
        {
            return $"#{CupNumber} => #{NextCup.CupNumber}";
        }
    }
}