using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day02bFail
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
        return CanBeMadeSafe(GetDifferences(inputLine));
    }

    private bool CanBeMadeSafe(List<int> differences)
    {
        int countPositive = differences.Count(n => n >= 0);
        int countNegative = differences.Count(n => n <= 0);
        if (countPositive == 0 || countNegative == 0)
        {            
            //all the same sign
            bool allInRange = differences.All(n =>  (Math.Abs(n) >= 1) && (Math.Abs(n) <= 3));
            if (allInRange)
            {
                //Console.WriteLine($"{inputLine} is ALREADY SAFE");
                //Console.WriteLine($"[{string.Join(' ', differences)}]");
                return true;
            }
        }
        else if (countPositive == 1)
        {
            List<int> newDifferences = RemoveSinglePositiveDifference(differences);

            if (IsSafe(newDifferences))
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        else if (countNegative == 1)
        {
            List<int> newDifferences = RemoveSingleNegativeDifference(differences);

            if (IsSafe(newDifferences))
            {
                return true;
            }
            else
            {
                return false;
            }

        }

        //Console.WriteLine($"{inputLine} is NOT SAFE");      
        //Console.WriteLine($"[{string.Join(' ', differences)}]");
        
        return false;
    }

    private static List<int> RemoveSinglePositiveDifference(List<int> differences)
    {
        List<int> newDifferences = [];

        int carryOver = 0;
        foreach (int difference in differences)
        {
            if (difference < 0)
            {
                newDifferences.Add(difference + carryOver);
                carryOver = 0;
            }
            else
            {
                carryOver = difference;
            }
        }

        return newDifferences;
    }

    private static List<int> RemoveSingleNegativeDifference(List<int> differences)
    {
        List<int> newDifferences = [];

        int carryOver = 0;
        foreach (int difference in differences)
        {
            if (difference > 0)
            {
                newDifferences.Add(difference + carryOver);
                carryOver = 0;
            }
            else
            {
                carryOver = difference;
            }
        }

        return newDifferences;
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
            if (CanBeMadeSafe(inputLine))
            {
                //Console.WriteLine($"{inputLine} CAN be made SAFE");    
                count += 1;
            }
            else
            {
                Console.WriteLine($"{inputLine} CANNOT be made SAFE");    
            }
        }
        return count;
    }

    private bool IsSafe(List<int> differences)
    {
        bool allPositive = differences.All(n => n > 0);
        bool allNegative = differences.All(n => n < 0);
        if (allPositive || allNegative)
        {            
            bool allInRange = differences.All(n =>  (Math.Abs(n) >= 1) && (Math.Abs(n) <= 3));
            if (allInRange)
            {
                //Console.WriteLine($"{inputLine} is SAFE");
                //Console.WriteLine($"[{string.Join(' ', differences)}]");
                return true;
            }
        }  
        //Console.WriteLine($"{inputLine} is NOT SAFE");      
        //Console.WriteLine($"[{string.Join(' ', differences)}]");
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
