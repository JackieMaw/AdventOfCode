[TestFixture]
public class Day01b
{
    private const int day = 1;
    private const int year = 2025;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void CanTurnLeftToZero()
    {        
        Assert.That(Execute(["L50"]), Is.EqualTo(1));
    }

    [Test]
    public void CanTurnRightToZero()
    {        
        Assert.That(Execute(["R50"]), Is.EqualTo(1));
    }

    [Test]
    public void FullTurnLeftPassesZeroOnce()
    {        
        Assert.That(Execute(["L100"]), Is.EqualTo(1));
    }

    [Test]
    public void FullTurnRightPassesZeroOnce()
    {        
        Assert.That(Execute(["R100"]), Is.EqualTo(1));
    }

    [Test]
    public void ThousandClicksLeftPassesZeroTenTimes()
    {        
        Assert.That(Execute(["L1000"]), Is.EqualTo(10));
    }

    [Test]
    public void ThousandClicksRightPassesZeroTenTimes()
    {        
        Assert.That(Execute(["R1000"]), Is.EqualTo(10));
    }

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 6;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 1031;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        int countTimesPassedZero = 0;

        int dialPosition = 50;
        Console.WriteLine("The dial starts by pointing at 50.");

        foreach (var line in input)
        {
            var direction = line[0];
            var fullMagnitude = Convert.ToInt32(line[1..]);
            var numberOfFullTurns = fullMagnitude / 100;
            var magnitude = fullMagnitude % 100;

            countTimesPassedZero += numberOfFullTurns;
            if (numberOfFullTurns > 0)
                Console.WriteLine($"   {numberOfFullTurns} x PASSES");

            switch (direction)
            {
                case 'L':
                    // turn left
                    dialPosition = dialPosition - magnitude;

                    if (dialPosition < 0)
                    {
                        dialPosition += 100;
                        countTimesPassedZero++;                        
                        Console.WriteLine($"   PASSED ZERO");
                    }

                    break;
                case 'R':
                    // turn right
                    dialPosition = dialPosition + magnitude;

                    if (dialPosition > 99)
                    {
                        dialPosition -= 100;
                        countTimesPassedZero++;
                        Console.WriteLine($"   PASSED ZERO");
                    }

                    break;
                default:
                    throw new Exception($"Unknown direction: {direction}");
            }
            
            Console.WriteLine($"The dial is rotated {line} to point at {dialPosition}.");
        }

        return countTimesPassedZero;
    }
}