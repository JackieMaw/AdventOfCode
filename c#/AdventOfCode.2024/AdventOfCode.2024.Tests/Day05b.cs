using System.Data;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day05b
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
        var expectedResult = 123;
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
        var badUpdates = GetBadUpdates(updateRules, pageUpdates);
        var correctUpdates = GetCorrectUpdates(badUpdates, updateRules);
        var result = GetSumOfMiddlePages(correctUpdates);
        return result;
    }

    private List<PageUpdate> GetCorrectUpdates(List<PageUpdate> badUpdates, List<UpdateRule> updateRules)
    {
        var dependencyGraph = GetDependencyGraph(updateRules);
        var topologicalOrder = GetTopologicalOrder(dependencyGraph);
        return badUpdates.Select(x => x.CorrectOrdering(topologicalOrder)).ToList();        
    }

    private Dictionary<string, Page> GetDependencyGraph(List<UpdateRule> updateRules)
    {
        Dictionary<string, Page> pageMap = [];

        foreach (var updateRule in updateRules)
        {
            Page before;
            if (!pageMap.TryGetValue(updateRule.Before, out before))
            {
                before = new Page(updateRule.Before);
                pageMap.Add(updateRule.Before, before);
            }
            Page after;
            if (!pageMap.TryGetValue(updateRule.After, out after))
            {
                after = new Page(updateRule.After);
                pageMap.Add(updateRule.After, after);
            }
            after.Prerequisites.Add(before);
        }

        return pageMap;        
    }

    private List<string> GetTopologicalOrder(Dictionary<string, Page> pageMap)
    {
        var mustVisit = pageMap.Values.ToList();

        var topologicalOrder = new List<string>();
        var alreadyVisited = new HashSet<string>();

        while(mustVisit.Count > 0)
        {
            Visit(mustVisit.First(), topologicalOrder, alreadyVisited, mustVisit);
        }

        return topologicalOrder;
    }

    private void Visit(Page currentPage, List<string> topologicalOrder, HashSet<string> alreadyVisited, List<Page> mustVisit)
    {
        foreach (var prerequisite in currentPage.Prerequisites)
        {
            if (!alreadyVisited.Contains(prerequisite.PageNumber))
            {
                Visit(prerequisite, topologicalOrder, alreadyVisited, mustVisit);
            }
        }
        topologicalOrder.Add(currentPage.PageNumber);
        alreadyVisited.Add(currentPage.PageNumber);
        mustVisit.Remove(currentPage);
    }

    private long GetSumOfMiddlePages(List<PageUpdate> goodUpdates)
    {
        return goodUpdates.Sum(x => x.GetMiddlePage());
    }

    private List<PageUpdate> GetBadUpdates(List<UpdateRule> updateRules, List<PageUpdate> pageUpdates)
    {
        var badUpdates = new List<PageUpdate>();
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
            if (!isGood)
                badUpdates.Add(pageUpdate); 
        }
        return badUpdates;
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

        public string Before { get; set; }
        public string After { get; set; }

        public UpdateRule(string inputLine)
        {
           var splitInputLine = inputLine.Split('|');
           Before = splitInputLine[0];
           After = splitInputLine[1];
        }

        public bool IsSatisfiedBy(PageUpdate pageUpdate)
        {
            bool alreadyFoundAfter = false;
            foreach (var update in pageUpdate.Updates)
            {
                if (update == After)
                {
                    alreadyFoundAfter = true;
                }
                else if (update == Before)
                {
                    if (alreadyFoundAfter) return false;
                    else return true;                    
                }
            }
            return true;
        }
    }

    private class Page
    {
        public string PageNumber { get; private set; }

        public Page(string pageNumber)
        {
            PageNumber = pageNumber;
            Prerequisites = new List<Page>();
        }

        public List<Page> Prerequisites { get; private set; }
    }

    private class PageUpdate
    {
        public List<string> Updates;
        

        public PageUpdate(string inputLine)
        {
            Updates = inputLine.Split(',').ToList();
        }

        public PageUpdate()
        {
            Updates = new List<string>();
        }

        public int GetMiddlePage()
        {
            var middlePage = Updates[Updates.Count / 2];
            Console.WriteLine($"Middle Page: {middlePage}");
            return Convert.ToInt32(middlePage);
        }

        public PageUpdate CorrectOrdering(List<string> topologicalOrder)
        {
            var correctedUpdate = new PageUpdate();
            foreach (var page in topologicalOrder)
            {
                if (Updates.Contains(page))
                {
                    correctedUpdate.Updates.Add(page);
                }
            }
            return correctedUpdate;
        }
    }
}
