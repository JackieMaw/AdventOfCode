using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day16a
{
    private const int day = 16;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void UnitTest_CheckThatPriorityQueueBehaves()
    {
        var thingToEnQ = new DirectedPosition(new Point(5, 5), Point.Right);
        var priorityQueue = new PriorityQueue<DirectedPosition, long>();
        priorityQueue.Enqueue(thingToEnQ, 0);

        var thingDeQ = priorityQueue.Dequeue();

        Assert.That(thingDeQ, Is.EqualTo(thingToEnQ));
    }    

    [Test]
    public void TestSampleInput_1()
    {
        Console.WriteLine("Testing Sample Input 1...");
        var expectedResult = 7036;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test1");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestSampleInput_2()
    {
        Console.WriteLine("Testing Sample Input 2...");
        var expectedResult = 11048;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test2");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 98520;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }    

    private readonly record struct DirectedPosition(Point Position, Point Direction)
    {
    }

    private long Execute(string[] input)
    {
        var map = Map.CreateMap(input);

        HashSet<DirectedPosition> alreadyExplored = [];
        var notExploredYet = new PriorityQueue<DirectedPosition, long>();
        var shortestPaths = new Dictionary<DirectedPosition, long>();

        Console.WriteLine($"Starting at {map.start} > {Point.Right}");
        var startingState = new DirectedPosition(map.start, Point.Right);
        notExploredYet.Enqueue(startingState, 0);
        shortestPaths.Add(startingState, 0);

        while(notExploredYet.Count > 0)
        {
            var exploreMeNow = notExploredYet.Dequeue();

            var pathToEnd = Explore(exploreMeNow, map, notExploredYet, shortestPaths, alreadyExplored);

            if (pathToEnd.HasValue)
                return pathToEnd.Value;

            alreadyExplored.Add(exploreMeNow);
        }
        
        throw new Exception("No path found :-( Methinks something went wrong!");
    }

    private long? Explore(DirectedPosition currentPosition, Map map, PriorityQueue<DirectedPosition, long> notExploredYet, Dictionary<DirectedPosition, long> shortestPaths, HashSet<DirectedPosition> alreadyExplored)
    {
        Console.WriteLine($"Exploring {currentPosition.Position} > {currentPosition.Direction}");

        var possibleMoves = GetPossibleMoves(currentPosition, map);

        foreach (var (newPosition, costToMove) in possibleMoves)
        {
            var costToGetHere = shortestPaths[currentPosition];
            var newCost = costToGetHere + costToMove;
            
            if (shortestPaths.ContainsKey(newPosition))
            {
                //if we have found this node before, then we need to check if this new path is shorter
                var currentCost = shortestPaths[newPosition];
                if (newCost < currentCost)
                {
                    shortestPaths[newPosition] = newCost;
                }
            }
            else
            {
                //if this is the first time we have found this node then this is the shortest path
                shortestPaths[newPosition] = newCost;

                if (newPosition.Position == map.end)
                {
                    return newCost;
                }
            }

            if (!alreadyExplored.Contains(newPosition))
            {
                notExploredYet.Enqueue(newPosition, newCost);
            }            
        }

        return null;
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
}
