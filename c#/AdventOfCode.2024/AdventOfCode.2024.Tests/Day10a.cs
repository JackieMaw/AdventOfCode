using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day10a
{
    private const int day = 10;
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
        var expectedResult = 36;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 531;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var heightMap = ParseInput(input);
        var trailHeads = GetAllTrailHeads(heightMap);
        return trailHeads.Sum(p => p.Item2);
    }

    private List<(Point, int)> GetAllTrailHeads(HeightMap heightMap)
    {
        List<(Point, int)> trailHeads = [];

        for (int y = 0;y < heightMap.Heights.GetLength(1); y++)
        for (int x = 0;x < heightMap.Heights.GetLength(0); x++)
        {
            Point point = new(x, y);
            if (heightMap.GetHeight(point) == 0)
            {
                int score = ClimbTrail(point, heightMap);
                if (score > 0)
                    trailHeads.Add((point, score));
            }
        }

        return trailHeads;
    }

    private int ClimbTrail(Point startingPoint, HeightMap heightMap)
    {
        HashSet<Point> currentPoints = [startingPoint];

        for (int expectedHeight = 1; expectedHeight <= 9; expectedHeight++)
        {
            HashSet<Point> newPoints = [];
            foreach (Point point in currentPoints)
            {
                IEnumerable<Point> neighbours = heightMap.GetNeighbours(point);
                IEnumerable<Point> goodNeighbours = neighbours.Where(n => heightMap.GetHeight(n) == expectedHeight);
                
                foreach (Point goodNeighbour in goodNeighbours)
                {
                    if (!newPoints.Contains(goodNeighbour))
                        newPoints.Add(goodNeighbour);
                }
            }
            currentPoints = newPoints;
        }

        return currentPoints.Count;
    }

    private HeightMap ParseInput(string[] input)
    {
        return new HeightMap(ReadInput.GetIntGrid(input));
    }
}
