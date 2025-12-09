

public class Day09b
{
    private const int day = 9;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void UnitTests()
    {
        var result = GetArea(new Point(2, 5), new Point(11, 1));
        var expectedResult = 50;
        Assert.That(result, Is.EqualTo(expectedResult));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 50;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 4759531084;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (allPoints, polygon) = ParseInput(input);
        var allDistances = GetAllDistances(allPoints);
        var (p1, p2) = GetLargestRectangleInside(allDistances, polygon);
        return GetArea(p1, p2);
    }

    private (Point p1, Point p2) GetLargestRectangleInside(PriorityQueue<(Point, Point), double> allDistances, Polygon polygon)
    {
        while (allDistances.Count > 0)
        {
            var (p1, p2) = allDistances.Dequeue();
            var rectangle = GetRectangle(p1, p2);
            if (polygon.Contains(rectangle))
            {
                return (p1, p2);
            }
        }
    }

    private Polygon GetRectangle(Point p1, Point p2)
    {
        var corner1 = new Point(p2.X, p1.Y);
        var corner2 = new Point(p1.X, p2.Y);
        return new Polygon(
        [
            new(p1, corner1),
            new(corner1, p2),
            new(p2, corner2),
            new(corner2, p1),
        ]);
    }

    private long GetArea(Point p1, Point p2)
    {
        long x = Math.Abs(p1.X - p2.X) + 1;
        long y = Math.Abs(p1.Y - p2.Y) + 1;
        return x * y;
    }

    private (List<Point>, Polygon) ParseInput(string[] input)
    {
        var allPoints = new List<Point>();
        var polygon = new Polygon();

        foreach (var line in input)
        {
            var parts = line.Split(',');
            var x = long.Parse(parts[0]);
            var y = long.Parse(parts[1]);

            Point point = new(x, y);
            if (allPoints.Count > 0)
            {
                Point previousPoint = allPoints[^1];
                polygon.edges.Add(new LineSegment(previousPoint, point));
            }
            allPoints.Add(point);
        }

        polygon.edges.Add(new LineSegment(allPoints[0], allPoints[^1]));

        return (allPoints, polygon);
    }

    private PriorityQueue<(Point, Point), double> GetAllDistances(List<Point> allPoints)
    {
        int count = allPoints.Count;
        var priorityQueue = new PriorityQueue<(Point, Point), double>();

        for (int i = 0; i < count; i++)
        {
            for (int j = 0; j < i; j++)
            {
                long area = GetArea(allPoints[i], allPoints[j]);
                Console.WriteLine($"Area between Point {i} and Point {j} = {area}");
                priorityQueue.Enqueue((allPoints[i], allPoints[j]), area * -1);
            }
        }

        return priorityQueue;
    }
}