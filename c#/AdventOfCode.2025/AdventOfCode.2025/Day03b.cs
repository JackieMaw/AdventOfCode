
public class Day03b
{
    private const int day = 3;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    /*
    In 987654321111111, the largest joltage can be found by turning on everything except some 1s at the end to produce 987654321111.
    In the digit sequence 811111111111119, the largest joltage can be found by turning on everything except some 1s, producing 811111111119.
    In 234234234234278, the largest joltage can be found by turning on everything except a 2 battery, a 3 battery, and another 2 battery near the start to produce 434234234278.
    In 818181911112111, the joltage 888911112111 is produced by turning on everything except some 1s near the front.
    The total output joltage is now much larger: 987654321111 + 811111111119 + 434234234278 + 888911112111 = 3121910778619.
    */

    [Test]
    public void UnitTests()
    {
        Assert.That(GetLargestJoltage("123456789999999"), Is.EqualTo(456789999999));
        Assert.That(GetLargestJoltage("987659876598765"), Is.EqualTo(989876598765));
        Assert.That(GetLargestJoltage("987654321111111"), Is.EqualTo(987654321111));
        Assert.That(GetLargestJoltage("811111111111119"), Is.EqualTo(811111111119));
        Assert.That(GetLargestJoltage("234234234234278"), Is.EqualTo(434234234278));
        Assert.That(GetLargestJoltage("818181911112111"), Is.EqualTo(888911112111));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 3121910778619;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 172162399742349;
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
        int lineLength = line.Length;
        int windowLength = lineLength - 12;

        int[] originalDigits = [.. line.Select(c => (int)char.GetNumericValue(c))];

        int[] finalDigits = new int[12];

        int lastConsumedPosition = -1;

        for (int digitCounter = 0; digitCounter < 12; digitCounter++)
        {
            int maxValueForThisPosition = -1;
            int positionOfMaxValue = -1;

            //find the best option for this digit position
            for (int position = lastConsumedPosition + 1; position <= digitCounter + windowLength; position++)
            {
                int thisDigit = originalDigits[position];

                if (thisDigit > maxValueForThisPosition)
                {
                    maxValueForThisPosition = thisDigit;
                    positionOfMaxValue = position;
                }
            }

            finalDigits[digitCounter] = maxValueForThisPosition;
            lastConsumedPosition = positionOfMaxValue;          
        }       

        return long.Parse(string.Concat(finalDigits));
    }
}