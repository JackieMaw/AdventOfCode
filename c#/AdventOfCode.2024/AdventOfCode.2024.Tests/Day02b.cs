using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day02b
{
    private const int day = 2;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void UnitTests()
    {
        Assert.Pass();
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 2;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 686;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        int count = 0;
        foreach (var inputLine in input)
        {
            if (IsSafe(inputLine))
                count += 1;
        }
        return count;
    }

    private bool IsSafe(string inputLine)
    {
        var differences = GetDifferences(inputLine);
        bool allPositive = differences.All(n => n > 0);
        bool allNegative = differences.All(n => n < 0);
        bool allInRange = differences.All(n =>  (Math.Abs(n) > 1) && (Math.Abs(n) <= 3));
        if ((allPositive || allNegative) && allInRange)
        {
            return true;
        }
        
        Console.WriteLine($"{inputLine} is SAFE");
        return false;
    }

    private List<int> GetDifferences(string inputLine)
    { 
        var differences = new List<int>();
        int? previousLevel = null;
        foreach (var levelString in inputLine.Split(' '))
        {
            int level = int.Parse(levelString);
            if (previousLevel != null)
            {
                differences.Add(level - previousLevel.Value);                
            }
            previousLevel = level;
        }
        return differences;
    }
}
