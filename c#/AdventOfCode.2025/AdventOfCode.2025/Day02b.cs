
public class Day02b
{
    private const int day = 2;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    /*
    11-22 still has two invalid IDs, 11 and 22.
    95-115 now has two invalid IDs, 99 and 111.
    998-1012 now has two invalid IDs, 999 and 1010.
    1188511880-1188511890 still has one invalid ID, 1188511885.
    222220-222224 still has one invalid ID, 222222.
    1698522-1698528 still contains no invalid IDs.
    446443-446449 still has one invalid ID, 446446.
    38593856-38593862 still has one invalid ID, 38593859.
    565653-565659 now has one invalid ID, 565656.
    824824821-824824827 now has one invalid ID, 824824824.
    2121212118-2121212124 now has one invalid ID, 2121212121.
    */

    [Test]
    public void UnitTests()
    {
        Assert.That(true, Is.EqualTo(IsValidId(1)));
        Assert.That(false, Is.EqualTo(IsValidId(11)));
        Assert.That(false, Is.EqualTo(IsValidId(111)));
        Assert.That(false, Is.EqualTo(IsValidId(1111)));
        Assert.That(false, Is.EqualTo(IsValidId(123123)));
        Assert.That(true, Is.EqualTo(IsValidId(1231234)));
        Assert.That(true, Is.EqualTo(IsValidId(12351234)));
        Assert.That(false, Is.EqualTo(IsValidId(123123123)));

        Assert.That(33, Is.EqualTo(SumInvalidIdsInRange("11-22")));
        Assert.That(1188511885, Is.EqualTo(SumInvalidIdsInRange("1188511880-1188511890")));
        Assert.That(0, Is.EqualTo(SumInvalidIdsInRange("1698522-1698528")));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 4174379265;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 73694270688;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        //11-22,95-115
        var totalSumOfInvalidIds = 0L;
        foreach (var numberRange in input[0].Split(','))
        {
            var sumOfInvalidIds = SumInvalidIdsInRange(numberRange);
            Console.WriteLine($"{numberRange} has {sumOfInvalidIds} invalid IDs");
            totalSumOfInvalidIds += sumOfInvalidIds;
        }
        return totalSumOfInvalidIds;
    }

    private long SumInvalidIdsInRange(string numberRange)
    {
        var sumOfInvalidIds = 0L;
        var rangeParts = numberRange.Split('-');
        var start = Convert.ToInt64(rangeParts[0]); 
        var end = Convert.ToInt64(rangeParts[1]);

        for (long id = start; id <= end; id++)
        {
            if (!IsValidId(id))
                sumOfInvalidIds += id;
        }
        return sumOfInvalidIds;
    }

    private bool IsValidId(long id)
    {
        var idString = id.ToString();

        var halfLength = idString.Length / 2;

        for (int segmentLength = 1; segmentLength <= halfLength; segmentLength++)
        {
            var segment = idString[..segmentLength];
            var repeatedSegment = string.Concat(Enumerable.Repeat(segment, idString.Length / segmentLength));
            if (repeatedSegment == idString)
            {
                return false;
            }
        }

        return true;
    }
}