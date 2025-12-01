[TestFixture]
public class Day01a
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
        var expectedResult = 0;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        int countTimesReturnedToZero = 0;

        int dialPosition = 50;
        Console.WriteLine("The dial starts by pointing at 50.");

        foreach (var line in input)
        {
            var direction = line[0];
            var magnitude = Convert.ToInt32(line[1..]);

            switch (direction)
            {
                case 'L':
                    // turn left
                    dialPosition = (dialPosition - magnitude) % 100;
                    break;
                case 'R':
                    // turn right
                    dialPosition = (dialPosition + magnitude) % 100;
                    break;
                default:
                    throw new Exception($"Unknown direction: {direction}");
            }

            Console.WriteLine($"The dial is rotated {line} to point at {dialPosition}.");

            if (dialPosition == 0)
            {
                countTimesReturnedToZero++;
            }
        }

        return countTimesReturnedToZero;
    }
}