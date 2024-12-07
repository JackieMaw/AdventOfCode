using System.Text.RegularExpressions;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day03a
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
        var expectedResult = 161;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 189527826;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        long result = 0;

        string pattern = @"mul\((\d+),(\d+)\)";

        Regex regex = new Regex(pattern);

        foreach (var inputLine in input)
        {
            Match match = regex.Match(inputLine);

            while (match.Success)
            {
                var x = Convert.ToInt32(match.Groups[1].Value);
                var y = Convert.ToInt32(match.Groups[2].Value);
                result += x * y;

                Console.WriteLine("Found match: " + match.Value);
                match = match.NextMatch();
            }
        }

        return result;
    }
}
