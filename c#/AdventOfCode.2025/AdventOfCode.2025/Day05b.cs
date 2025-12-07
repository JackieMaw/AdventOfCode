


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
        var expectedResult = 346240317247002;
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
        ranges.Sort();

        var optimizedRanges = new List<(long, long)>();

        (long start, long end) previousRange = (-1, -1);

        foreach ((long start, long end) range in ranges)
        {
            if (previousRange.start == -1)
            {
                previousRange = range;
            }
            else
            {                
                //NO OVERLAP
                if (range.start > previousRange.end)
                {
                    //SAVE THE PREVIOUS RANGE
                    optimizedRanges.Add(previousRange);
                    previousRange = range;
                }
                else //MERGE RANGES
                {                    
                    previousRange.end = Math.Max(previousRange.end, range.end);                    
                }
            }
        }

        //SAVE THE LAST RANGE
        optimizedRanges.Add(previousRange);

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