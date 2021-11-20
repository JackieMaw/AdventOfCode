using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day13
{
    class Program
    {
        static void Main(string[] args)
        {
            var inputs = ReadInput.GetStrings("Input.txt");
            long answer = PartTwoWithJumps(inputs);
            Console.WriteLine($"answer = {answer}");
        }

        private static long PartTwoWithJumps(string[] inputs)
        {
            var busIds = inputs[1].Split(',');
            IEnumerable<Tuple<int, int>> busses = GetBusRules(busIds);
                        
            long timestamp = 0;
            long jumpsize = 0;
            foreach (var bus in busses)
            {
                int busId = bus.Item1;
                int offSet = bus.Item2;

                Console.WriteLine($"Looking for {busId} @ offset {offSet}...");

                if (jumpsize == 0)
                {
                    jumpsize = bus.Item1;
                }
                else
                {
                    //keep jumping
                    Console.WriteLine($"jumpsize = {jumpsize}");
                    bool found = false;
                    while (!found)
                    {
                        timestamp += jumpsize;
                        if ((timestamp + offSet) % busId == 0)
                            found = true;
                    }

                    jumpsize *= bus.Item1;
                }
            }
            return timestamp;            
        }

        private static long PartTwo_Slow(string[] inputs)
        {
            var busIds = inputs[1].Split(',');
            IEnumerable<Tuple<int, int>> busses = GetBusRules(busIds);

            int firstBusId = Convert.ToInt32(busIds[0]);
            for (long i = 0; true; i++)
            {
                long startingTimestamp = firstBusId * i;

                bool success = DoTheBusesFit(startingTimestamp, busses);

                if (success)
                    return startingTimestamp;

                if ((i % 1000000) == 0)
                    Console.WriteLine($"iteration {i}");
            }
        }

        private static bool DoTheBusesFit(long startingTimestamp, IEnumerable<Tuple<int, int>> busses)
        {
            foreach (var bus in busses)
            {
                int busId = bus.Item1;
                int offSet = bus.Item2;
                if (((startingTimestamp + offSet) % busId) != 0)
                {
                    return false;
                }
            }

            return true;
        }

        private static IEnumerable<Tuple<int, int>> GetBusRules(string[] busIds)
        {
            for (int i = 0; i < busIds.Length; i++)
            {
                if (busIds[i] != "x")
                {
                    yield return new Tuple<int, int>(Convert.ToInt32(busIds[i]), i);
                }
            }
        }

        private static void PartOne(string[] inputs)
        {
            int timestampToLeave = Convert.ToInt32(inputs[0]);
            var busses = inputs[1].Split(',').Where(s => s != "x").Select(s => Convert.ToInt32(s));

            int commonMultiple = GetCommonMultiple(busses);
            Console.WriteLine($"commonMultiple = {commonMultiple}"); //this is how often the busses will syncronise    

            int lastSyncPoint = timestampToLeave - (timestampToLeave % commonMultiple);

            int answer = GetAnswer(busses.Select(b => new Tuple<int, int>(b, GetNextBus(lastSyncPoint, b, timestampToLeave))), timestampToLeave);

            Console.WriteLine($"answer = {answer}");
        }

        private static int GetAnswer(IEnumerable<Tuple<int, int>> nextBusses, int timestampToLeave)
        {
            int minBusTime = Int32.MaxValue;
            int minBusId = 0;

            foreach (var nextBus in nextBusses)
            {
                var busId = nextBus.Item1;
                var busTime = nextBus.Item2;

                if (busTime < minBusTime)
                {
                    minBusTime = busTime;
                    minBusId = busId;
                }
            }

            return minBusId * (minBusTime - timestampToLeave);
        }

        private static int GetNextBus(int lastSyncPoint, int busId, int timestampToLeave)
        {
            int lastBusTime = lastSyncPoint;
            while (lastBusTime < timestampToLeave)
            {
                lastBusTime += busId;
            }
            return lastBusTime;
        }

        private static DateTime GetStartTime()
        {
            List<Tuple<int, DateTime>> busTimes = new List<Tuple<int, DateTime>> () 
            {
                new Tuple<int, DateTime>(7, DateTime.Today.AddHours(9).AddMinutes(31)),
                new Tuple<int, DateTime>(13, DateTime.Today.AddHours(9).AddMinutes(36)),
                new Tuple<int, DateTime>(59, DateTime.Today.AddHours(9).AddMinutes(44)),
                new Tuple<int, DateTime>(31, DateTime.Today.AddHours(9).AddMinutes(30)),
                new Tuple<int, DateTime>(19, DateTime.Today.AddHours(9).AddMinutes(31)),
            };

            int commonMultiple = GetCommonMultiple(busTimes.Select(t => t.Item1));
            Console.WriteLine($"commonMultiple = {commonMultiple}"); //this is how often the busses will syncronise            

            var commonBusTimesInThePast = IntersectAll(busTimes.Select(b => GetAllPreviousTimes(b, commonMultiple))).ToArray();

            Array.Sort(commonBusTimesInThePast);

            return commonBusTimesInThePast[commonBusTimesInThePast.Length - 1];
        }


        private static IEnumerable<DateTime> GetAllPreviousTimes(Tuple<int, DateTime> bus, int maxMinutesToSearch)
        {
            var busId = bus.Item1;
            DateTime? busTime = bus.Item2;
            for (int i = 1; i <= maxMinutesToSearch / busId ; i++)
            {
                try
                {
                    busTime = busTime.Value.AddMinutes(busId * i * -1);
                }
                catch (Exception)
                {
                    busTime = null;
                }

                if (busTime.HasValue)
                    yield return busTime.Value;
                else
                    yield break;
                
            }
        }

        private static int GetLowestCommonMultiple(IEnumerable<int> numbers)
        {
            int highestMultiple = GetCommonMultiple(numbers);

            var commonMultiples = IntersectAll(numbers.Select(n => GetMultiples(n, highestMultiple))).ToArray();
            Array.Sort(commonMultiples);
            return commonMultiples[0];
        }

        private static int GetCommonMultiple(IEnumerable<int> numbers)
        {
            int highestMultiple = 1;
            foreach (var n in numbers)
            {
                highestMultiple *= n;
            }

            return highestMultiple;
        }

        private static IEnumerable<T> IntersectAll<T>(IEnumerable<IEnumerable<T>> allListsOfNumbers)
        {
            IEnumerable<T> result = null; ;
            foreach (var listOfNumbers in allListsOfNumbers)
            {
                if (result == null)
                    result = listOfNumbers;
                else
                    result = result.Intersect(listOfNumbers);

            }
            return result;
        }

        private static IEnumerable<int> GetMultiples(int n, int highestMultiple)
        {
            for (int i = 1; i <= highestMultiple / n; i++)
            {
                yield return n * i;
            }
        }
    }
}
