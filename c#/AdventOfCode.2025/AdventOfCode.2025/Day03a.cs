
public class Day03a
{
    private const int day = 3;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    /*
    In 987654321111111, you can make the largest joltage possible, 98, by turning on the first two batteries.
    In 811111111111119, you can make the largest joltage possible by turning on the batteries labeled 8 and 9, producing 89 jolts.
    In 234234234234278, you can make 78 by turning on the last two batteries (marked 7 and 8).
    In 818181911112111, the largest joltage you can produce is 92.
    The total output joltage is the sum of the maximum joltage from each bank, so in this example, the total output joltage is 98 + 89 + 78 + 92 = 357.
    */

    [Test]
    public void UnitTests()
    {
        Assert.That(11, Is.EqualTo(GetLargestJoltage("11")));
        Assert.That(11, Is.EqualTo(GetLargestJoltage("111")));
        Assert.That(11, Is.EqualTo(GetLargestJoltage("1111")));
        Assert.That(89, Is.EqualTo(GetLargestJoltage("89")));
        Assert.That(98, Is.EqualTo(GetLargestJoltage("98")));
        Assert.That(91, Is.EqualTo(GetLargestJoltage("18191")));
        Assert.That(98, Is.EqualTo(GetLargestJoltage("19181")));

        Assert.That(98, Is.EqualTo(GetLargestJoltage("987654321111111")));
        Assert.That(89, Is.EqualTo(GetLargestJoltage("811111111111119")));
        Assert.That(78, Is.EqualTo(GetLargestJoltage("234234234234278")));
        Assert.That(92, Is.EqualTo(GetLargestJoltage("818181911112111")));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 357;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 17301;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        long sumOfLargestJoltage = 0;
        foreach (var line in input)
        {
            var largestJoltageForThisLine = GetLargestJoltage(line);
            sumOfLargestJoltage += largestJoltageForThisLine;
            Console.WriteLine($"{line} => {largestJoltageForThisLine}");
        }
        return sumOfLargestJoltage;
    }

    private long GetLargestJoltage(string line)
    {
        int firstDigit = (int)char.GetNumericValue(line[0]);
        int lastDigit = (int)char.GetNumericValue(line[line.Length - 1]);
        int secondDigit = lastDigit;

        for (int position = 1; position < line.Length - 1; position++)
        {
            int thisDigit = (int)char.GetNumericValue(line[position]);
            if (thisDigit > firstDigit)
            {
                firstDigit = thisDigit;
                secondDigit = lastDigit;
            }
            else if (thisDigit > secondDigit)
            {
                secondDigit = thisDigit;
            }
        }

        return firstDigit * 10 + secondDigit;
    }
}