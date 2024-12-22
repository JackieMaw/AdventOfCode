using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day18b
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
        var expectedResult = "6,1";
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input, 6);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = "46,23";
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input, 70);
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

    private string Execute(string[] input, int gridSize)
    {
        var allObstacles = ParseInput(input);

        for (int i = 0; i < allObstacles.Count; i++)
        {
            Console.WriteLine($"Number of Obstacles = {i} >> ");

            var obstacles = allObstacles.Take(i + 1).ToHashSet();
            var map = new Map(obstacles, gridSize + 1, gridSize + 1);
            
            long? shortestPath = GetLengthOfShortestPath(gridSize, map);
            if (!shortestPath.HasValue)
            {
                var lastObstacle = allObstacles.Skip(i).First();
                var result =  $"{lastObstacle.X},{lastObstacle.Y}";
                return result;
            }
        }

        throw new Exception("No obstacle found :-( Methinks something went wrong!");
    }

    private long? GetLengthOfShortestPath(int gridSize, Map map)
    {
        HashSet<Point> alreadyExplored = [];
        var notExploredYet = new PriorityQueue<Point, long>();
        var shortestPaths = new Dictionary<Point, long>();

        var start = new Point(0, 0);
        var end = new Point(gridSize, gridSize);

        long costToGetHereFromStart = 0;
        long costToGetToEndFromHere = GetHeuristicScore(start, end);
        var score = costToGetHereFromStart + costToGetToEndFromHere;
        notExploredYet.Enqueue(start, score);
        shortestPaths.Add(start, costToGetHereFromStart);

        while (notExploredYet.Count > 0)
        {
            var exploreMeNow = notExploredYet.Dequeue();
            alreadyExplored.Add(exploreMeNow);

            var pathToEnd = Explore(exploreMeNow, map, notExploredYet, shortestPaths, alreadyExplored, end);

            if (pathToEnd.HasValue)
                return pathToEnd.Value;
        }

        return null;
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

                var costToGetToEndFromHere = GetHeuristicScore(newPosition, end);
                var score = costToGetToNewPosition + costToGetToEndFromHere;
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
