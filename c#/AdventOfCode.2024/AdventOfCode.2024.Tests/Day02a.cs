using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day02a
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
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 686;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
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
        int? previousLevel = null;
        bool? increasing = null;
        foreach (var levelString in inputLine.Split(' '))
        {
            int level = int.Parse(levelString);
            if (previousLevel != null)
            {
                var diff = level - previousLevel.Value;
                var absDiff = Math.Abs(diff);

                if ((absDiff < 1) || (absDiff > 3))
                    return false;

                if (increasing.HasValue)
                {
                    if (increasing.Value)
                    {
                        if (diff < 0) 
                            return false;
                    }
                    else
                    {
                        if (diff > 0) 
                            return false;
                    }
                }
                else
                {
                    increasing = diff > 0;
                }
            }
            Console.WriteLine($"{level} is OK");
            previousLevel = level;
        }
        Console.WriteLine($"{inputLine} is SAFE");
        return true;
    }
}
