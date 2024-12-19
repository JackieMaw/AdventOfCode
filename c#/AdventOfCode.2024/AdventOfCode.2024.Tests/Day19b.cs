using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day19b
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
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var (towelsAvailable, desiredPatterns) = ParseInput(input);

        var expectedResult = 1;
        var result = CountNumberOfPossiblePatterns(towelsAvailable, ["r"]);
        Assert.That(result, Is.EqualTo(expectedResult));

        expectedResult = 2;
        result = CountNumberOfPossiblePatterns(towelsAvailable, ["br"]);
        Assert.That(result, Is.EqualTo(expectedResult));

        expectedResult = 3;
        result = CountNumberOfPossiblePatterns(towelsAvailable, ["gbr"]);
        Assert.That(result, Is.EqualTo(expectedResult));

        expectedResult = 3;
        result = CountNumberOfPossiblePatterns(towelsAvailable, ["bgbr"]);
        Assert.That(result, Is.EqualTo(expectedResult));

        expectedResult = 6;
        result = CountNumberOfPossiblePatterns(towelsAvailable, ["rbgbr"]);
        Assert.That(result, Is.EqualTo(expectedResult));

        expectedResult = 6;
        result = CountNumberOfPossiblePatterns(towelsAvailable, ["rrbgbr"]);
        Assert.That(result, Is.EqualTo(expectedResult));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 16;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 616957151871345;
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
        Dictionary<string, long> possibilitiesCache = PreCache(towelsAvailable);

        long sumNumPossibilities = 0;

        foreach (var pattern in desiredPatterns)
        {
            Console.WriteLine($"{pattern} >>>");
            var numPossibilities = GetNumPossibilities(pattern, towelsAvailable, possibilitiesCache, pattern.Length);
            Console.WriteLine($"{pattern} has {numPossibilities} possible configurations");
            sumNumPossibilities += numPossibilities;
        }

        return sumNumPossibilities;
    }

    private Dictionary<string, long> PreCache(string[] towelsAvailable)
    {
        Dictionary<string, long> possibilitiesCache = [];

        foreach (string towel in towelsAvailable.OrderBy(x => x.Length))
        {
            if (towel.Length == 1)
                possibilitiesCache.Add(towel, 1);
            else
                GetNumPossibilities(towel, towelsAvailable, possibilitiesCache, towel.Length);
        }

        return possibilitiesCache;
    }

    private long GetNumPossibilities(string pattern, string[] towelsAvailable, Dictionary<string, long> possibilitiesCache, int displayLength)
    {
        if (pattern.Length == 0)
            return 1;

        if (possibilitiesCache.ContainsKey(pattern))
        {
            long numPossibilitiesFromCache = possibilitiesCache[pattern];            
            Console.WriteLine($"*CACHE HIT* {pattern} has {numPossibilitiesFromCache}");

            return numPossibilitiesFromCache;
        }
        
        long numPossibilities = GetNumPossibilitiesImpl(pattern, towelsAvailable, possibilitiesCache, displayLength);

        possibilitiesCache[pattern] = numPossibilities;
        Console.WriteLine($"*CACHE FILL* {pattern} has {numPossibilities}");

        return numPossibilities;
    }

    private long GetNumPossibilitiesImpl(string pattern, string[] towelsAvailable, Dictionary<string, long> possibilitiesCache, int displayLength)
    {
        Console.WriteLine($"{pattern.PadLeft(displayLength)}");

        long numPossibilities = 0;

        foreach (var towel in towelsAvailable)
        {            
            //Console.WriteLine($"{towel}?");

            if (pattern.StartsWith(towel))
            {
                //Console.WriteLine($"{towel}!");

                string restOfPattern = pattern.Substring(towel.Length);

                numPossibilities += GetNumPossibilities(restOfPattern, towelsAvailable, possibilitiesCache, displayLength);
            }
        }

        return numPossibilities;
    }

    private (string[] towelsAvailable, string[] desiredPatterns) ParseInput(string[] input)
    {
        string[] towelsAvailable = input[0].Split(',', StringSplitOptions.TrimEntries);
        string[] desiredPatterns = input.Skip(2).ToArray();
        return (towelsAvailable, desiredPatterns);
    }
}
