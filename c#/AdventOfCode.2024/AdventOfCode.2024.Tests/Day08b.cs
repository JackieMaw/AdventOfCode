using System.ComponentModel.DataAnnotations;
using System.Security.Cryptography;
using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day08b
{
    private const int day = 8;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void Test_GetAllPointsOnLine_Gradient_1()
    {
        var points = GetAllPointsOnLine(new Point(5,5), new Point(7,7), 10, 10);
        Assert.That(points.Count, Is.EqualTo(10));
        Assert.That(points.Contains(new Point(1,1)));
    }    

    [Test]
    public void Test_GetAllPointsOnLine_Gradient_minus1()
    {
        var points = GetAllPointsOnLine(new Point(5,5), new Point(3,7), 10, 10);
        Assert.That(points.Count, Is.EqualTo(9));
        Assert.That(points.Contains(new Point(4,6)));
    } 
    [Test]
    public void Test_GetAllPointsOnLine_Gradient_half()
    {
        var points = GetAllPointsOnLine(new Point(5,5), new Point(6,7), 10, 10);
        Assert.That(points.Count, Is.EqualTo(5));
        Assert.That(points.Contains(new Point(3,1)));
    }    

    [Test]
    public void Test_GetAllPointsOnLine_Gradient_minusHalf()
    {
        var points = GetAllPointsOnLine(new Point(5,5), new Point(4,7), 10, 10);
        Assert.That(points.Count, Is.EqualTo(5));
        Assert.That(points.Contains(new Point(7,1)));
    }

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 34;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestSampleInput2()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 9;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test2");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 367;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (antennaLocationsByChar, maxX, maxY) = ParseInput(input);

        HashSet<Point> allAntiNodes = [];
        foreach (var antennaLocations in antennaLocationsByChar)
        {
            var antiNodes = GetAntinodes(antennaLocations.Value, maxX, maxY);
            System.Console.WriteLine($"{antiNodes.Count()} antiNodes found for {antennaLocations.Key}");
            allAntiNodes.UnionWith(antiNodes);
        }

        DisplayNodes(allAntiNodes, maxX, maxY);

        return allAntiNodes.Count;
    }

    private void DisplayNodes(HashSet<Point> allAntiNodes, int maxX, int maxY)
    {
        for (int y = 0; y < maxY; y++)
        {
            for (int x = 0; x < maxX; x++)
            {
                if (allAntiNodes.Contains(new Point(x, y)))
                {
                    Console.Write("#");
                }
                else
                {                    
                    Console.Write(".");
                }
            }
            System.Console.WriteLine();
        }
    }

    private IEnumerable<Point> GetAntinodes(List<Point> antennaLocations, int maxX, int maxY)
    {
        List<Point> antiNodes = [];

        HashSet<(Point, Point)> locationsAlreadyExplored = [];

        foreach (var location1 in antennaLocations)
        foreach (var location2 in antennaLocations)
        {
            if ((location1 != location2)&&(!locationsAlreadyExplored.Contains((location2, location1))))
                {
                    locationsAlreadyExplored.Add((location1, location2));

                    var allPointsOnLine = GetAllPointsOnLine(location1, location2, maxX, maxY);

                    antiNodes.AddRange(allPointsOnLine);
                }
            }

        return antiNodes.Distinct();
    }

    private static List<Point> GetAllPointsOnLine(Point location1, Point location2, int maxX, int maxY)
    {
        List<Point> points = [];

        double deltaX = location2.X - location1.X;
        double deltaY = location2.Y - location1.Y;
        double gradient = deltaX / deltaY;

        for (int x2 = 0; x2 < maxX; x2++) //try all possible values of x
        {            
            var newDeltaX = location1.X - x2;
            double newDeltaY = newDeltaX / gradient;

            if (newDeltaY % 1 == 0)
            {
                int y2 = (int)(location1.Y - newDeltaY);
                if ((y2 >= 0)&&(y2 < maxY))
                {
                    points.Add(new Point(x2, y2));
                }
            }
        }

        return points;
    }

    private (Dictionary<char, List<Point>>, int, int) ParseInput(string[] input)
    {
        Dictionary<char, List<Point>> antennaLocations = [];

        int maxY = input.Length;
        int maxX = input[0].Length;

        for (int y = 0; y < input.Length; y++)
        {
            var inputLine = input[y];
            for (int x = 0; x < inputLine.Length; x++)
            {
                char antennaCharacter = inputLine[x];
                if (antennaCharacter != '.')
                {
                    if (!antennaLocations.TryGetValue(antennaCharacter, out var listOfLocations))
                    {
                        listOfLocations = new List<Point>();
                        antennaLocations[antennaCharacter] = listOfLocations;
                    }
                    listOfLocations.Add(new Point(x, y));
                }
            }
        }

        return (antennaLocations, maxX, maxY);
    }

    private readonly record struct Point(int X, int Y)
    {
        public static Point Up = new(0, -1);
        public static Point Right = new(1, 0);
        public static Point Down = new(0, 1);
        public static Point Left = new(-1, 0);
    }

}
