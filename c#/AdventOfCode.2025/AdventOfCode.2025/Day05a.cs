


public class Day05a
{
    private const int day = 5;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void UnitTests()
    {
        var result = 0;
        var expectedResult = 0;
        Assert.That(result, Is.EqualTo(expectedResult));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 3;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 896;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (ranges, itemIds) = ParseInput(input);
        return CountFreshItems(ranges, itemIds);
    }

    private ((long, long) [] ranges, long [] itemIds) ParseInput(string[] input)
    {
        var ranges = new List<(long, long)>();
        var itemIds = new List<long>();

        int lineCounter = 0;
        while (input[lineCounter] != "")
        {
            var parts = input[lineCounter].Split('-');
            var range = (long.Parse(parts[0]), long.Parse(parts[1]));
            ranges.Add(range);
            lineCounter++;
        }

        for (int i = lineCounter + 1; i < input.Length; i++)
        {
            itemIds.Add(long.Parse(input[i]));
        }

        return (ranges.ToArray(), itemIds.ToArray());
    }


    private long CountFreshItems((long, long)[] ranges, long[] itemIds)
    {
        long numberOfFreshIds = 0;

        foreach (var itemId in itemIds)
        {
            foreach (var (start, end) in ranges)
            {
                if (itemId >= start && itemId <= end)
                {
                    //this item is fresh
                    numberOfFreshIds++;
                    break; //stop looking
                }
            }
        }

        return numberOfFreshIds;
    }
}