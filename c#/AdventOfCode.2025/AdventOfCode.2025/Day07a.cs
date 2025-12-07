public class Day07a
{
    private const int day = 7;
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
        var expectedResult = 21;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 1626;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        long countBeamSplits = 0;
        var output = input.ToCharArray2D();
        for (int rowIndex = 0; rowIndex < output.GetLength(0) - 1; rowIndex++)
        {
            for (int colIndex = 0; colIndex < output.GetLength(1); colIndex++)
            {
                var ch = output[rowIndex,colIndex];
                if (ch == 'S')
                {               
                    Console.WriteLine($"S at row {rowIndex}, col {colIndex}");
                    output.TrySetValue('|', rowIndex + 1, colIndex);
                }
                else if (ch == '|')
                {
                    var nextCh = output[rowIndex + 1,colIndex];
                    if (nextCh == '^')
                    {
                        countBeamSplits++;                    
                        Console.WriteLine($"Beam split at row {rowIndex}, col {colIndex}");
                        output.TrySetValue('|', rowIndex + 1, colIndex - 1);
                        output.TrySetValue('|', rowIndex + 1, colIndex + 1);                        
                    }
                    else
                    {
                        output.TrySetValue('|', rowIndex + 1, colIndex);
                    }
                }
            }
        }
        return countBeamSplits;
    }
}