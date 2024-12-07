using System.Text.RegularExpressions;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day03b
{
    private const int day = 3;
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
        var expectedResult = 48;
        var input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 63013756;
        var input = aocSupplier.GetPuzzleInput_SingleLine(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string input)
    {
        Dictionary<int, (long?, bool?)> resultAtIndex = [];
        PopulateMultiplications(input, resultAtIndex);
        PopulateDisable(input, resultAtIndex);
        PopulateEnable(input, resultAtIndex);

        long result = 0;
        bool enabled = true;
        foreach (var index in resultAtIndex.Keys.Order())
        {
            var (product, enable) = resultAtIndex[index];
            if (enable.HasValue)
            {
                enabled = enable.Value;
            }
            else if (enabled)
            {
                if (product.HasValue)
                    result += product.Value;
                else
                    throw new Exception("Value expected");
            }
        }

        return result;
    }

    private static void PopulateMultiplications(string input, Dictionary<int, (long?, bool?)> resultAtIndex)
    {
        string pattern = @"mul\((\d+),(\d+)\)";
        Regex regex = new(pattern, RegexOptions.Singleline);

        Match match = regex.Match(input);

        while (match.Success)
        {
            var x = Convert.ToInt32(match.Groups[1].Value);
            var y = Convert.ToInt32(match.Groups[2].Value);
            resultAtIndex[match.Index] = (x * y, null);

            Console.WriteLine("Found match: " + match.Value);
            match = match.NextMatch();
        }
        
    }

    

    private static void PopulateDisable(string input, Dictionary<int, (long?, bool?)> resultAtIndex)
    {
        string pattern = @"don't\(\)";
        Regex regex = new(pattern, RegexOptions.Singleline);

        Match match = regex.Match(input);

        while (match.Success)
        {
            resultAtIndex[match.Index] = (null, false);

            Console.WriteLine("Found match: " + match.Value);
            match = match.NextMatch();
        }
    }

    private static void PopulateEnable(string input, Dictionary<int, (long?, bool?)> resultAtIndex)
    {
        string pattern = @"do\(\)";
        Regex regex = new(pattern, RegexOptions.Singleline);
        
        Match match = regex.Match(input);

        while (match.Success)
        {
            resultAtIndex[match.Index] = (null, true);

            Console.WriteLine("Found match: " + match.Value);
            match = match.NextMatch();
        }
    }
}
