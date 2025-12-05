


public class Day05b
{
    private const int day = 5;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void CanMergeMultipleRanges()
    {
        List<(long, long)> ranges =
        [
            (30, 40),
            (35, 55),
            (50, 60)
        ];

        List<(long, long)> expectedOptimizedRanges =
        [
            (30, 60)
        ];

        var actualOptimizedRanges = OptimizeRanges(ranges);
        Assert.That(actualOptimizedRanges, Has.Exactly(1).Items);  
        Assert.That(actualOptimizedRanges, Is.EqualTo(expectedOptimizedRanges));     
    } 

    [Test]
    public void CanMergeMultipleRangesInDifferentOrder()
    {
        List<(long, long)> ranges =
        [
            (30, 40),
            (50, 60),
            (35, 55),
        ];

        List<(long, long)> expectedOptimizedRanges =
        [
            (30, 60)
        ];

        var actualOptimizedRanges = OptimizeRanges(ranges);
        Assert.That(actualOptimizedRanges, Has.Exactly(1).Items);  
        Assert.That(actualOptimizedRanges, Is.EqualTo(expectedOptimizedRanges));        
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 14;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 0;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var ranges = ParseInput(input);
        var optimizedRanges = OptimizeRanges(ranges);
        return CountFreshItems(optimizedRanges);
    }

    private List<(long, long)> OptimizeRanges(List<(long, long)> ranges)
    {
        Console.WriteLine($"Starting with {ranges.Count} ranges...");
        var optimizedRanges = OptimizeRangesOnce(ranges);
        Console.WriteLine($"Optimized to {optimizedRanges.Count} ranges");
        while (optimizedRanges.Count < ranges.Count)
        {
            ranges = optimizedRanges;
            optimizedRanges = OptimizeRangesOnce(ranges);
            Console.WriteLine($"Optimized to {optimizedRanges.Count} ranges");
        }
        Console.WriteLine("===NO FURTHER OPTIMIZATION ACHIEVED===");
        return optimizedRanges;
    }

    private List<(long, long)> OptimizeRangesOnce(List<(long, long)> ranges)
    {
        ranges.Sort();

        var optimizedRanges = new List<(long, long)>();

        foreach (var (startNewRange, endNewRange) in ranges)
        {
            bool isOverLapping = false;
            foreach (var (startExistingRange, endExistingRange) in optimizedRanges)
            {
                //case 1: NO OVERLAP
                if (startExistingRange > endNewRange || startNewRange > endExistingRange)
                {
                    //DO NOTHING, ignore this existing range and check the next one
                    continue;
                }
                else
                {
                    isOverLapping = true;
                    if (startNewRange <= startExistingRange && endNewRange >= endExistingRange)
                    {
                        //case 2A: FULL OVERLAP - new range can replace the existing range
                        optimizedRanges.Remove((startExistingRange, endExistingRange));
                        optimizedRanges.Add((startExistingRange, endExistingRange));
                    }
                    else if (startExistingRange <= startNewRange && endExistingRange >= endNewRange)
                    {
                        //case 2A: FULL OVERLAP - existing range already contains the new range
                        //DO NOTHING
                    }
                    else if (startNewRange <= startExistingRange && endNewRange < endExistingRange)
                    {
                        //case 3A: PARTIAL OVERLAP - new range comes first
                        optimizedRanges.Remove((startExistingRange, endExistingRange));
                        optimizedRanges.Add((startNewRange, endExistingRange));
                    }
                    else if (startExistingRange < startNewRange && endExistingRange < endNewRange)
                    {
                        //case 3B: PARTIAL OVERLAP - existing range comes first
                        optimizedRanges.Remove((startExistingRange, endExistingRange));
                        optimizedRanges.Add((startExistingRange,  endNewRange));
                    }
                    else
                    {
                        throw new Exception("Unhandled overlap case");
                    }
                    break; //exit the loop through existing ranges because we already found one
                }
                
            }
            if (!isOverLapping)
            {
                optimizedRanges.Add((startNewRange, endNewRange));
            }
        }

        return optimizedRanges;
    }

    private List<(long, long)> ParseInput(string[] input)
    {
        var ranges = new List<(long, long)>();

        int lineCounter = 0;
        while (input[lineCounter] != "")
        {
            var parts = input[lineCounter].Split('-');
            var range = (long.Parse(parts[0]), long.Parse(parts[1]));
            ranges.Add(range);
            lineCounter++;
        }

        return ranges;
    }


    private long CountFreshItems(List<(long, long)> ranges)
    {
        long numberOfFreshIds = 0;

        foreach (var (start, end) in ranges)
        {
            numberOfFreshIds += end - start + 1;
        }

        return numberOfFreshIds;
    }
}