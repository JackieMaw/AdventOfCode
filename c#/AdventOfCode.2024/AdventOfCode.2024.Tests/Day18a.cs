using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day18a
{
    private const int day = 18;
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
        var expectedResult = 22;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input, 6, 12);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 0;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input, 70, 1024);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private HashSet<Point> ParseInput(IEnumerable<string> input)
    {
        HashSet<Point> obstacles = [];

        foreach (var inputLine in input)
        {
            var lineParts = inputLine.Split(',');
            obstacles.Add(new Point(Convert.ToInt32(lineParts[0]),Convert.ToInt32(lineParts[1])));
        }

        return obstacles;
    }

    private long Execute(string[] input, int gridSize, int numIterations)
    {
        var obstacles = ParseInput(input.Take(numIterations));

        var map = new Map(obstacles, gridSize+1, gridSize+1);

        HashSet<Point> alreadyExplored = [];
        var notExploredYet = new PriorityQueue<Point, long>();
        var shortestPaths = new Dictionary<Point, long>();

        var start = new Point(0, 0);
        var end = new Point(gridSize, gridSize);
        Console.WriteLine($"Starting at {start} >");

        long costToGetHereFromStart = 0;
        var costToGetToEndFromHere = GetHeuristicScore(start, end);
        var score = costToGetHereFromStart + costToGetToEndFromHere;
        notExploredYet.Enqueue(start, score);
        shortestPaths.Add(start, costToGetHereFromStart);

        while(notExploredYet.Count > 0)
        {
            var exploreMeNow = notExploredYet.Dequeue();
            alreadyExplored.Add(exploreMeNow);

            Console.WriteLine();
            Console.WriteLine($"Exploring {exploreMeNow} >> (alreadyExplored = {alreadyExplored.Count}, notExploredYet = {notExploredYet.Count})");
            Console.WriteLine();

            var pathToEnd = Explore(exploreMeNow, map, notExploredYet, shortestPaths, alreadyExplored, end);

            if (pathToEnd.HasValue)
                return pathToEnd.Value;
        }
        
        throw new Exception("No path found :-( Methinks something went wrong!");
    }

    private long? Explore(Point currentPosition, Map map, PriorityQueue<Point, long> notExploredYet, Dictionary<Point, long> shortestPaths, HashSet<Point> alreadyExplored, Point end)
    {
        var possibleMoves = map.GetNeighbours(currentPosition);

        foreach (var newPosition in possibleMoves.OrderBy(p => GetHeuristicScore(p, end)))
        {
            var costToGetHere = shortestPaths[currentPosition];
            var costToGetToNewPosition = costToGetHere + 1;
            
            if (shortestPaths.ContainsKey(newPosition))
            {
                //if we have found this node before, then we need to check if this new path is shorter
                var currentCost = shortestPaths[newPosition];
                if (costToGetToNewPosition < currentCost)
                {
                    shortestPaths[newPosition] = costToGetToNewPosition;
                }
            }
            else
            {
                //if this is the first time we have found this node then this is the shortest path
                shortestPaths[newPosition] = costToGetToNewPosition;

                if (newPosition == end)
                {
                    return costToGetToNewPosition;
                }
            }

            if (!alreadyExplored.Contains(newPosition))
            {
                Point removed;
                long priority;
                notExploredYet.Remove(newPosition, out removed, out priority);

                long costToGetToEndFromHere = GetHeuristicScore(newPosition, end);
                var score = costToGetToNewPosition + costToGetToEndFromHere;
                
                Console.WriteLine($"     Adding {newPosition} to Q with score: {score} >> (neighbour of {currentPosition})");

                notExploredYet.Enqueue(newPosition, score);
            }            
        }

        return null;
    }

    private long GetHeuristicScore(Point newPosition, Point end)
    {
        return Math.Abs(newPosition.X - end.X) + Math.Abs(newPosition.Y + end.Y);
    }
}
