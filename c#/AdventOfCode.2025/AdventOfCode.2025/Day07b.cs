
public class Day07b
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
        var expectedResult = 40;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 48989920237096;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var output = input.ToCharArray2D();
        var timelineCounterGrid = new long[output.GetLength(0), output.GetLength(1)];
        for (int rowIndex = 0; rowIndex < output.GetLength(0) - 1; rowIndex++)
        {
            for (int colIndex = 0; colIndex < output.GetLength(1); colIndex++)
            {
                var ch = output[rowIndex,colIndex];
                var numberOfTimelines = timelineCounterGrid[rowIndex, colIndex];
                if (ch == 'S')
                {
                    timelineCounterGrid[rowIndex, colIndex] = 1;
                    Console.WriteLine($"S at row {rowIndex}, col {colIndex}");
                    output.TrySetValue('|', rowIndex + 1, colIndex);
                    timelineCounterGrid.TrySetValue(1, rowIndex  + 1, colIndex);
                }
                else if (ch == '|')
                {
                    var nextCh = output[rowIndex + 1,colIndex];
                    if (nextCh == '^')
                    {                 
                        Console.WriteLine($"Beam split at row {rowIndex}, col {colIndex}");

                        if (colIndex - 1 >= 0)
                        {
                            output[rowIndex + 1, colIndex - 1] = '|';
                            timelineCounterGrid[rowIndex  + 1, colIndex - 1] += numberOfTimelines;
                        }

                        if (colIndex + 1 < output.GetLength(1))
                        {
                            output[rowIndex + 1, colIndex + 1] = '|';
                            timelineCounterGrid[rowIndex  + 1, colIndex + 1] += numberOfTimelines;  
                        }                
                    }
                    else
                    {
                            output[rowIndex + 1, colIndex] = '|';
                        timelineCounterGrid[rowIndex  + 1, colIndex] += numberOfTimelines;  
                    }
                }
            }
            var sumOfTimelinesForThisRow = SumRow(timelineCounterGrid, rowIndex + 1);
            Console.WriteLine($"Row #{rowIndex + 1} sum of timelines: {sumOfTimelinesForThisRow}");
        }
        return SumRow(timelineCounterGrid, timelineCounterGrid.GetLength(0) - 1);
    }

    private long SumRow(long[,] timelineCounterGrid, int rowIndex)
    {
        long sum = 0;
        for (int colIndex = 0; colIndex < timelineCounterGrid.GetLength(1); colIndex++)
        {
            sum += timelineCounterGrid[rowIndex, colIndex];
        }
        return sum;
    }
}