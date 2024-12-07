using System.Data;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day06a
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
        var expectedResult = 41;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 4758;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (obstacles, startingPosition, mapWidth, mapLength) = ParseInput(input);

        HashSet<Point> visited = [];

        var position = startingPosition;
        Console.WriteLine($"Starting at {position}");
        var direction = Point.Up;
        while (IsWithinRange(position, mapWidth, mapLength))
        {
            var nextPosition = Move(position, direction);
            while (obstacles.Contains(nextPosition))
            {
                direction = TurnRight(direction);                
                Console.WriteLine($"Turned Right...");
                nextPosition = Move(position, direction);
            }
            position = nextPosition;
            visited.Add(position);
            Console.WriteLine($"Moved to {position}");
        }
        return visited.Count - 1;
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
        public static Point Up = new(0, -1);
        public static Point Right = new(1, 0);
        public static Point Down = new(0, 1);
        public static Point Left = new(-1, 0);
    }

}
