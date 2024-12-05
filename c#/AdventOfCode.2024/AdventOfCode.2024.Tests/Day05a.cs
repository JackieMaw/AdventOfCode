using System.Data;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day05a
{
    private const int day = 5;
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
        var expectedResult = 143;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 0;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    private long Execute(string[] input)
    {
        var (updateRules, pageUpdates) = ParseInput(input);
        var goodUpdates = GetGoodUpdates(pageUpdates);
        var result = GetSumOfMiddlePages(goodUpdates);
    }

    private (List<UpdateRule> updateRules, List<PageUpdate> pageUpdates) ParseInput(string[] input)
    {
        List<UpdateRule> updateRules = [];
        List<PageUpdate> pageUpdates = [];

        foreach (var inputLine in input)
        {
            if (inputLine.Contains("|"))
        }

        return (updateRules, pageUpdates);
    }

    private class UpdateRule
    {
    }

    private class PageUpdate
    {
    }
}
