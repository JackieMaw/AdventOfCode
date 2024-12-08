using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day08a
{
    private const int day = 8;
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
        var expectedResult = 14;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
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
        foreach (var antennaLocations in antennaLocationsByChar.Values)
        {
            var antiNodes = GetAntinodes(antennaLocations, maxX, maxY);
            allAntiNodes.UnionWith(antiNodes);
        }

        return allAntiNodes.Count;
    }

    private IEnumerable<Point> GetAntinodes(List<Point> antennaLocations, int maxX, int maxY)
    {
        List<Point> antiNodes = [];

        foreach (var location1 in antennaLocations)
            foreach (var location2 in antennaLocations)
            {
                if (location1 != location2)
                {
                    var deltaX = location2.X - location1.X;
                    var deltaY = location2.Y - location1.Y;

                    var antinode1 = new Point(location2.X + deltaX, location2.Y + deltaY);
                    var antinode2 = new Point(location1.X - deltaX, location1.Y - deltaY);

                    antiNodes.Add(antinode1);
                    antiNodes.Add(antinode2);
                }
            }

        return antiNodes.Where(p => p.X >= 0 && p.X < maxX && p.Y >= 0 && p.Y < maxY);
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

    private readonly record struct Point(double X, double Y)
    {
        public static Point Up = new(0, -1);
        public static Point Right = new(1, 0);
        public static Point Down = new(0, 1);
        public static Point Left = new(-1, 0);
    }

}
