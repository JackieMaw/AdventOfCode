using System;
using System.Collections.Generic;
using System.Linq;

namespace Day23
{
    class Program
    {
        static void Main(string[] args)
        {
            (var currentCup, var cupFinder) = SetupCups();

            for (int i = 1; i <= 10000000; i++)
            {
                if (i % 10000 == 0)
                {
                    Console.WriteLine($"--move {i}--");
                    //Console.WriteLine($"({currentCup.GetAllCups()})");
                    Console.WriteLine($"current: {currentCup.CupNumber}");
                }

                Stack<Cup> removedCups = new Stack<Cup>();
                for (int r = 0; r < 3; r++)
                {
                    removedCups.Push(currentCup.RemoveNextCup());
                }

                var destinationCupNumber = currentCup.CupNumber - 1;
                if (destinationCupNumber == 0)
                    destinationCupNumber = 1000000;

                while (removedCups.Any(c => c.CupNumber == destinationCupNumber))
                {
                    destinationCupNumber -= 1;
                    if (destinationCupNumber == 0)
                        destinationCupNumber = 1000000;
                }

                var destinationCup = cupFinder[destinationCupNumber];

                if (i % 10000 == 0)
                {
                    Console.WriteLine($"destination: {destinationCup.CupNumber}");
                }

                for (int r = 0; r < 3; r++)
                {
                    destinationCup.InsertCup(removedCups.Pop());
                }

                currentCup = currentCup.NextCup;
            }

            var cup1 = cupFinder[1];
            var cup2 = cup1.NextCup;
            var cup3 = cup2.NextCup;

            long answer = cup2.CupNumber * cup3.CupNumber;
            Console.WriteLine($"{answer} = {cup2.CupNumber} x {cup3.CupNumber}");

            //Console.WriteLine();
            //Console.WriteLine($"({currentCup.GetAllCups()})");
        }

        //private static Cup FindCup(Cup currentCup, long destinationCupNumber)
        //{
        //    while(currentCup.CupNumber != destinationCupNumber)
        //    {
        //        currentCup = currentCup.NextCup;
        //    }
        //    return currentCup;
        //}

        private static (Cup currentCup, Dictionary<long, Cup> cupFinder) SetupCups()
        {
            //389125467
            //157623984
            //int[] cups = new int[] { 3, 8, 9, 1, 2, 5, 4, 6, 7 };
            int[] cups = new int[] { 1,5,7,6,2,3,9,8,4 };

            Dictionary<long, Cup> cupFinder = new Dictionary<long, Cup>();

            Cup currentCup = null;
            Cup previousCup = null;

            foreach (var cupNumber in cups)
            {
                var cup = new Cup(cupNumber);
                cupFinder.Add(cupNumber, cup);

                if (currentCup == null)
                    currentCup = cup;

                if (previousCup != null)
                    previousCup.NextCup = cup;

                previousCup = cup;
            }

            for (long cupNumber = cups.Max() + 1; cupNumber <= 1000000; cupNumber++)
            {
                var cup = new Cup(cupNumber);
                cupFinder.Add(cupNumber, cup);

                if (currentCup == null)
                    currentCup = cup;

                if (previousCup != null)
                    previousCup.NextCup = cup;

                previousCup = cup;
            }

            previousCup.NextCup = currentCup;
            
            return (currentCup, cupFinder);
        }
    }
}
