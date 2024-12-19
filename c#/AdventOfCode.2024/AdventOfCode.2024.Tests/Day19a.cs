using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day19a
{
    private const int day = 19;
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
        var expectedResult = 6;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 251;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (towelsAvailable, desiredPatterns) = ParseInput(input);

        long numPossible = CountNumberOfPossiblePatterns(towelsAvailable, desiredPatterns);

        return numPossible;
    }

    private long CountNumberOfPossiblePatterns(string[] towelsAvailable, string[] desiredPatterns)
    {
        long numPossible = 0;
        long numImpossible = 0;

        Dictionary<string, bool> possibilitiesCache = [];

        foreach (string towel in towelsAvailable)
        {
            possibilitiesCache.Add(towel, true);
        }

        foreach (var pattern in desiredPatterns)
        {
            if (CheckIfPossible(pattern, towelsAvailable, possibilitiesCache))
            {
                numPossible++;
            }
            else
            {
                numImpossible++;
            }
        }
        
        return numPossible;
    }

    private bool CheckIfPossible(string pattern, string[] towelsAvailable, Dictionary<string, bool> possibilitiesCache)
    {
        if (possibilitiesCache.ContainsKey(pattern))
            return possibilitiesCache[pattern];
        
        bool isPossible = CalculateIfPossible(pattern, towelsAvailable, possibilitiesCache);

        possibilitiesCache[pattern] = isPossible;

        return isPossible;
    }

    private bool CalculateIfPossible(string pattern, string[] towelsAvailable, Dictionary<string, bool> possibilitiesCache)
    {
        Console.WriteLine(pattern);

        foreach (var towel in towelsAvailable)
        {
            if (pattern.StartsWith(towel))
            {
                string restOfPattern = pattern.Substring(towel.Length);

                if (restOfPattern.Length == 0)
                    return true;
                
                if (CheckIfPossible(restOfPattern, towelsAvailable, possibilitiesCache))
                    return true;
            }
        }

        return false;
    }

    private (string[] towelsAvailable, string[] desiredPatterns) ParseInput(string[] input)
    {
        string[] towelsAvailable = input[0].Split(',', StringSplitOptions.TrimEntries);
        string[] desiredPatterns = input.Skip(2).ToArray();
        return (towelsAvailable, desiredPatterns);
    }
}
