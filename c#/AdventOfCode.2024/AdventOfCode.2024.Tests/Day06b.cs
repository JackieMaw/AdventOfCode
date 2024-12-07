using System.Data;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day06b
{
    private const int day = 6;
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
        var expectedResult = 1670;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (obstacles, startingPosition, maxX, maxY) = ParseInput(input);

        var possibleObstables = GetPossibleObstacles(obstacles, startingPosition, maxX, maxY);
        int numSuccessfulNewObstacles = 0;    
        foreach (var newObstacle in possibleObstables)
        {
            obstacles.Add(newObstacle);
            if (GuardGotStuckInALoop(obstacles, startingPosition, maxX, maxY))
            {
                numSuccessfulNewObstacles++;
            }
            obstacles.Remove(newObstacle);
        }        
        return numSuccessfulNewObstacles;
    }

     private HashSet<Point> GetPossibleObstacles(HashSet<Point> obstacles, Point startingPosition, int maxX, int maxY)
    {
        HashSet<Point> visited = [];
        
        Dictionary<Point, HashSet<Point>> directionsByPosition = [];

        var position = startingPosition;
        Console.WriteLine($"Starting at {position}");
        var direction = Point.Up;
        while (IsWithinRange(position, maxX, maxY))
        {
            var nextPosition = Move(position, direction);
            while (obstacles.Contains(nextPosition))
            {
                direction = TurnRight(direction);
                Console.WriteLine($"Turned Right...");
                nextPosition = Move(position, direction);
            }
            position = nextPosition;
            Console.WriteLine($"Moved to {position}");

            if (!visited.Contains(position))
                visited.Add(position);

            if (!directionsByPosition.TryGetValue(position, out HashSet<Point>? directions))
            {
                directions = [direction];
                directionsByPosition.Add(position, directions);
            }
            else
            {
                if (directions.Contains(direction))
                {
                    throw new Exception("Guard got stuck in a loop!"); //we've been down this road before!
                }
                else
                {
                    directions.Add(direction);
                }
            }
        }

        return visited;
    }

    private bool GuardGotStuckInALoop(HashSet<Point> obstacles, Point startingPosition, int maxX, int maxY)
    {
        HashSet<Point> visited = [];
        
        Dictionary<Point, HashSet<Point>> directionsByPosition = [];

        var position = startingPosition;
        Console.WriteLine($"Starting at {position}");
        var direction = Point.Up;
        while (IsWithinRange(position, maxX, maxY))
        {
            var nextPosition = Move(position, direction);
            while (obstacles.Contains(nextPosition))
            {
                direction = TurnRight(direction);
                Console.WriteLine($"Turned Right...");
                nextPosition = Move(position, direction);
            }
            position = nextPosition;
            Console.WriteLine($"Moved to {position}");

            if (!visited.Contains(position))
                visited.Add(position);
                
            if (!directionsByPosition.TryGetValue(position, out HashSet<Point>? directions))
            {
                directions = [direction];
                directionsByPosition.Add(position, directions);
            }
            else
            {
                if (directions.Contains(direction))
                {
                    return true; //we've been down this road before!
                }
                else
                {
                    directions.Add(direction);
                }
            }
        }

        return false;
    }

    private Point TurnRight(Point direction)
    {
        if (direction == Point.Up) return Point.Right;
        if (direction == Point.Right) return Point.Down;
        if (direction == Point.Down) return Point.Left;
        if (direction == Point.Left) return Point.Up;
        throw new Exception($"Unexpected Direction: {direction}");
    }

    private Point Move(Point position, Point direction)
    {
        return new Point(position.X + direction.X, position.Y + direction.Y);
    }

    private bool IsWithinRange(Point currentPosition, int maxX, int maxY)
    {
        return (currentPosition.X >= 0) && (currentPosition.Y >= 0) && (currentPosition.X < maxX) && (currentPosition.Y < maxY);
    }

    private (HashSet<Point>, Point, int, int) ParseInput(string[] input)
    {
        HashSet<Point> obstacles = [];
        Point? startingPosition = null;

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
                    
                    case '^': startingPosition = new Point(x, y);
                    break;

                    case '.': break;

                    default: throw new Exception($"Unexpected Input: {inputLine[x]}");
                }
            }
        }

        if (!startingPosition.HasValue)
        {
            throw new Exception("Didn't find a starting position");
        }

        return (obstacles, startingPosition.Value, maxX, maxY);
    }

    private readonly record struct Point(double X, double Y)
    {
        public static Point Up = new Point(0, -1);
        public static Point Right = new Point(1, 0);
        public static Point Down = new Point(0, 1);
        public static Point Left = new Point(-1, 0);
    }

}
