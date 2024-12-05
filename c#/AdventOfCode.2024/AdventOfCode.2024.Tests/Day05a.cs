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
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 5087;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (updateRules, pageUpdates) = ParseInput(input);
        var goodUpdates = GetGoodUpdates(updateRules, pageUpdates);
        var result = GetSumOfMiddlePages(goodUpdates);
        return result;
    }

    private long GetSumOfMiddlePages(List<PageUpdate> goodUpdates)
    {
        return goodUpdates.Sum(x => x.GetMiddlePage());
    }

    private List<PageUpdate> GetGoodUpdates(List<UpdateRule> updateRules, List<PageUpdate> pageUpdates)
    {
        var goodUpdates = new List<PageUpdate>();
        foreach (var pageUpdate in pageUpdates)
        {
            bool isGood = true;
            foreach (var updateRule in updateRules)
            {
                if (!updateRule.IsSatisfiedBy(pageUpdate))
                {
                    isGood = false;
                    break;
                }
            }
            if (isGood)
                goodUpdates.Add(pageUpdate); 
        }
        return goodUpdates;
    }

    private (List<UpdateRule> updateRules, List<PageUpdate> pageUpdates) ParseInput(string[] input)
    {
        List<UpdateRule> updateRules = [];
        List<PageUpdate> pageUpdates = [];

        foreach (var inputLine in input)
        {
            if (inputLine.Contains("|"))
                updateRules.Add(new UpdateRule(inputLine));
            else if (inputLine != "")
                pageUpdates.Add(new PageUpdate(inputLine));
        }

        return (updateRules, pageUpdates);
    }

    private class UpdateRule
    {
        private int _before;
        private int _after;

        public UpdateRule(string inputLine)
        {
           var splitInputLine = inputLine.Split('|');
           _before = Convert.ToInt32(splitInputLine[0]);
           _after = Convert.ToInt32(splitInputLine[1]);
        }

        public bool IsSatisfiedBy(PageUpdate pageUpdate)
        {
            bool alreadyFoundAfter = false;
            foreach (var update in pageUpdate.Updates)
            {
                if (update == _after)
                {
                    alreadyFoundAfter = true;
                }
                else if (update == _before)
                {
                    if (alreadyFoundAfter) return false;
                    else return true;                    
                }
            }
            return true;
        }
    }

    private class PageUpdate
    {
        public List<int> Updates;

        public PageUpdate(string inputLine)
        {
            Updates = inputLine.Split(',').Select(x => Convert.ToInt32(x)).ToList();
        }

        internal int GetMiddlePage()
        {
            var middlePage = Updates[Updates.Count / 2];
            Console.WriteLine($"Middle Page: {middlePage}");
            return middlePage;
        }
    }
}
