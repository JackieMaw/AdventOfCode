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
    public void TestDoubleCount()
    {        
        Assert.That(Execute(["R50","L5"]), Is.EqualTo(1));
    }


    /*
    The dial starts by pointing at 50.
    The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
    The dial is rotated L30 to point at 52.
    The dial is rotated R48 to point at 0.
    The dial is rotated L5 to point at 95.
    The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
    The dial is rotated L55 to point at 0.
    The dial is rotated L1 to point at 99.
    The dial is rotated L99 to point at 0.
    The dial is rotated R14 to point at 14.
    The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.

    The dial starts by pointing at 50.
    PASSED ZERO => The dial is rotated L68 to point at 82.
    The dial is rotated L30 to point at 52.
    PASSED ZERO => The dial is rotated R48 to point at 0.
    PASSED ZERO => The dial is rotated L5 to point at 95.
   PASSED ZERO
The dial is rotated R60 to point at 55.
   EXACTLY AT ZERO
The dial is rotated L55 to point at 0.
   PASSED ZERO
The dial is rotated L1 to point at 99.
   EXACTLY AT ZERO
The dial is rotated L99 to point at 0.
The dial is rotated R14 to point at 14.
   PASSED ZERO
The dial is rotated L82 to point at 32.
Result: 8
    */

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
        var expectedResult = 5831;
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

                    var alreadyAtZero = dialPosition == 0;

                    // turn left
                    dialPosition = dialPosition - magnitude;

                    if (dialPosition == 0)
                    {
                        countTimesPassedZero++;                        
                        Console.WriteLine($"   EXACTLY AT ZERO");
                    }
                    else if (dialPosition < 0)
                    {
                        dialPosition += 100;
                        if (!alreadyAtZero)
                        {
                            countTimesPassedZero++;                        
                            Console.WriteLine($"   PASSED ZERO");
                        }
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