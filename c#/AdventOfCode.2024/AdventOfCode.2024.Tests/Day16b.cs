using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day16b
{
    private const int day = 16;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void TestSampleInput_1()
    {
        Console.WriteLine("Testing Sample Input 1...");
        var expectedResult = 45;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test1");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestSampleInput_2()
    {
        Console.WriteLine("Testing Sample Input 2...");
        var expectedResult = 64;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test2");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 609;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }    
    private long Execute(string[] input)
    {
        var (shortestPaths, endPositions) = GetAllBestPaths(input);

        HashSet<Point> allPointsOnPath = GetAllPointsOnBestPaths(shortestPaths, endPositions);
        
        return allPointsOnPath.Count;
    }

    private HashSet<Point> GetAllPointsOnBestPaths(Dictionary<DirectedPosition, PathInfo> shortestPaths, HashSet<DirectedPosition> endPositions)
    {
        HashSet<Point> allPoints = [];
        HashSet<DirectedPosition> allPositions = [];

        foreach (var position in endPositions)
        {
            Console.WriteLine($"GetAllPointsOnBestPaths {position.Position} > {position.Direction}");
            GetAllPointsOnPath(position, shortestPaths, allPoints, allPositions);
        }

        return allPoints;
    }

    private static void GetAllPointsOnPath(DirectedPosition position, Dictionary<DirectedPosition, PathInfo> shortestPaths, HashSet<Point> allPoints, HashSet<DirectedPosition> allPositions)
    {
        if (allPositions.Contains(position))
            return; //we have already explored this position = point + direction

        if (!allPoints.Contains(position.Position))
            allPoints.Add(position.Position);

        var pathInfo = shortestPaths[position];
        foreach (var predecessor in pathInfo.Predecessors)
        {
            GetAllPointsOnPath(predecessor, shortestPaths, allPoints, allPositions);
        }        
    }

    private (Dictionary<DirectedPosition, PathInfo> shortestPaths, HashSet<DirectedPosition> endPositions) GetAllBestPaths(string[] input)
    {
        var (map, start, end) = CreateMap(input);

        HashSet<DirectedPosition> alreadyExplored = [];
        var notExploredYet = new PriorityQueue<DirectedPosition, long>();
        var shortestPaths = new Dictionary<DirectedPosition, PathInfo>();
        var endPositions = new HashSet<DirectedPosition>();

        Console.WriteLine($"Starting at {start} > {Point.Right}");
        var startingState = new DirectedPosition(start, Point.Right);
        notExploredYet.Enqueue(startingState, 0);
        shortestPaths.Add(startingState, (0, new HashSet<DirectedPosition>()));

        while (notExploredYet.Count > 0)
        {
            var exploreMeNow = notExploredYet.Dequeue();

            Explore(exploreMeNow, map, notExploredYet, shortestPaths, alreadyExplored, endPositions, end);

            alreadyExplored.Add(exploreMeNow);
        }

        //remove any endPositions which are non-optimal
        var minCost = endPositions.Min(p => shortestPaths[p].Cost);
        endPositions = endPositions.Where(p => shortestPaths[p].Cost == minCost).ToHashSet();

        return (shortestPaths, endPositions);
    }

     private (Map map, Point start, Point end) CreateMap(string[] input)
    {
        HashSet<Point> obstacles = [];
        Point? start = null;
        Point? end = null;

        int maxY = input.Length;
        int maxX = input[0].Length;

        for (int y = 0; y < input.Length; y++)
        {
            var inputLine = input[y];
            for (int x = 0; x < inputLine.Length; x++)
            {
                switch (inputLine[x])
                {
                    case '#': obstacles.Add(new Point(x, y));
                    break;
                    
                    case 'S': start = new Point(x, y);
                    break;
                    
                    case 'E': end = new Point(x, y);
                    break;

                    case '.': break;

                    default: throw new Exception($"Unexpected Input: {inputLine[x]}");
                }
            }
        }

        if (!start.HasValue)
        {
            throw new Exception("Didn't find a starting position");
        }

        if (!end.HasValue)
        {
            throw new Exception("Didn't find an ending position");
        }

        return (new Map(obstacles, maxX, maxY), start.Value, end.Value);
    }

    private void Explore(DirectedPosition currentPosition, Map map, PriorityQueue<DirectedPosition, long> notExploredYet, Dictionary<DirectedPosition, PathInfo> shortestPaths, HashSet<DirectedPosition> alreadyExplored, HashSet<DirectedPosition> endPositions, Point end)    
    {
        Console.WriteLine($"Exploring {currentPosition.Position} > {currentPosition.Direction}");

        var possibleMoves = GetPossibleMoves(currentPosition, map);

        foreach (var (newPosition, costToMove) in possibleMoves)
        {
            var (costToGetHere, howToGetHere) = shortestPaths[currentPosition];
            var newCost = costToGetHere + costToMove;
            
            if (shortestPaths.ContainsKey(newPosition))
            {
                //if we have found this node before, then we need to check if this new path is shorter
                var (costToGetToNewPosition, howToGetToNewPosition) = shortestPaths[newPosition];
                if (newCost < costToGetToNewPosition)
                {
                    //this new path is shorter
                    shortestPaths[newPosition] = (newCost, new HashSet<DirectedPosition>() { currentPosition });
                }
                else if (newCost == costToGetToNewPosition)
                {
                    //this new path is the same, so we have found another good way
                    if (!howToGetToNewPosition.Contains(currentPosition))
                        howToGetToNewPosition.Add(currentPosition);
                }
            }
            else
            {
                //if this is the first time we have found this node then this is the shortest path
                shortestPaths[newPosition] = (newCost, new HashSet<DirectedPosition>() { currentPosition });

                if (newPosition.Position == end)
                {
                    if (!endPositions.Contains(newPosition))
                        endPositions.Add(newPosition);
                }
            }

            if (!alreadyExplored.Contains(newPosition))
            {
                notExploredYet.Enqueue(newPosition, newCost);
            }            
        }
    }

    private List<(DirectedPosition, long)> GetPossibleMoves(DirectedPosition currentPosition, Map map)
    {  
        var possibleMoves = new List<(DirectedPosition, long)>();

        var direction = currentPosition.Direction;

        var nextPosition = map.Move(currentPosition.Position, direction);
        if (nextPosition.HasValue)
        {
            possibleMoves.Add((new DirectedPosition(nextPosition.Value, direction), 1));
        }

        direction = Map.TurnRight(direction); //90 degrees clockwise = 1000 cost
        nextPosition = map.Move(currentPosition.Position, direction);
        if (nextPosition.HasValue)
        {
            possibleMoves.Add((new DirectedPosition(nextPosition.Value, direction), 1001));
        }

        direction = Map.TurnRight(direction); //180 degrees clockwise = 2000 cost
        nextPosition = map.Move(currentPosition.Position, direction);
        if (nextPosition.HasValue)
        {
            possibleMoves.Add((new DirectedPosition(nextPosition.Value, direction), 2001));
        }

        direction = Map.TurnRight(direction); //180 degrees counter-clockwise = 1000 cost
        nextPosition = map.Move(currentPosition.Position, direction);
        if (nextPosition.HasValue)
        {
            possibleMoves.Add((new DirectedPosition(nextPosition.Value, direction), 1001));
        }

        return possibleMoves;
    }    

    readonly record struct DirectedPosition(Point Position, Point Direction);

    readonly record struct PathInfo(long Cost, HashSet<DirectedPosition> Predecessors)
    {
        public static implicit operator (long, HashSet<DirectedPosition>)(PathInfo value)
        {
            return (value.Cost, value.Predecessors);
        }

        public static implicit operator PathInfo((long, HashSet<DirectedPosition>) value)
        {
            return new PathInfo(value.Item1, value.Item2);
        }
    }
}



