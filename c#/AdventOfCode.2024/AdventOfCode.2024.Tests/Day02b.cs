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
        /*7 6 4 2 1: Safe without removing any level.
        1 2 7 8 9: Unsafe regardless of which level is removed.
        9 7 6 2 1: Unsafe regardless of which level is removed.
        1 3 2 4 5: Safe by removing the second level, 3.
        8 6 4 4 1: Safe by removing the third level, 4.
        1 3 6 7 9: Safe without removing any level.
        */

        Assert.That(CanBeMadeSafe("7 6 4 2 1"), Is.EqualTo(true));
        Assert.That(CanBeMadeSafe("1 2 7 8 9"), Is.EqualTo(false));
        Assert.That(CanBeMadeSafe("1 3 2 4 5"), Is.EqualTo(true));        
    }

    private bool CanBeMadeSafe(string inputLine)
    {
        var numbers = GetNumbers(inputLine);

        for (int i = 0; i < numbers.Count; i++)
        {
            List<int> listCopy = [.. numbers];
            listCopy.RemoveAt(i);
            if (IsSafe(listCopy))
                return true;
        }

        return false;
    }

    private List<int> GetNumbers(string inputLine)
    {
        return inputLine.Split(' ').Select(x => int.Parse(x)).ToList();
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 4;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 717;
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
            if (CanBeMadeSafe(inputLine))
            {
                //Console.WriteLine($"{inputLine} CAN be made SAFE");    
                count += 1;
            }
            else
            {
                //Console.WriteLine($"{inputLine} CANNOT be made SAFE");    
            }
        }
        return count;
    }

    private bool IsSafe(List<int> numbers)
    {
        var differences = GetDifferences(numbers);
        bool allPositive = differences.All(n => n > 0);
        bool allNegative = differences.All(n => n < 0);
        if (allPositive || allNegative)
        {            
            bool allInRange = differences.All(n =>  (Math.Abs(n) >= 1) && (Math.Abs(n) <= 3));
            if (allInRange)
            {
                return true;
            }
        }  
        return false;
    }

    private List<int> GetDifferences(List<int> numbers)
    { 
        var differences = new List<int>();
        int? previousLevel = null;
        foreach (var level in numbers)
        {
            if (previousLevel != null)
            {
                differences.Add(level - previousLevel.Value);                
            }
            previousLevel = level;
        }
        return differences;
    }
}
