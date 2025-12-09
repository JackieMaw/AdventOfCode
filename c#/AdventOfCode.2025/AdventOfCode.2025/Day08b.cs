
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
        var expectedResult = 25272;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 9271575747;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var allPoints = ParseInput(input);
        var result = ConnectClosestPoints(allPoints);
        return result;
    }

    private List<Point3d> ParseInput(string[] input)
    {
        var allPoints = new List<Point3d>();

        foreach (var line in input)
        {
            var parts = line.Split(',');
            var x = long.Parse(parts[0]);
            var y = long.Parse(parts[1]);
            var z = long.Parse(parts[2]);

            allPoints.Add(new Point3d(x, y, z));
        }

        return allPoints;
    }

    private long ConnectClosestPoints(List<Point3d> allPoints)
    {
        var allCircuits = new List<List<int>>();
        var priorityQueue = GetAllDistances(allPoints);

        var circuitMap = new Dictionary<int, List<int>>();

        int counter = 0;
        int numPossibleEdges = priorityQueue.Count;
        while (priorityQueue.Count > 0)
        {
            counter++;
            var (p1, p2) = priorityQueue.Dequeue();
            Console.WriteLine($"({counter} of {numPossibleEdges}) Adding Connection: {p1} <==> {p2}");
            //DisplayCircuits(allCircuits);
            //CASE 1: BOTH POINTS ARE NOT IN A CIRCUIT
            if (!circuitMap.ContainsKey(p1) && (!circuitMap.ContainsKey(p2)))
            {
                var newCircuit = new List<int> { p1, p2 };
                circuitMap[p1] = newCircuit;
                circuitMap[p2] = newCircuit;
                allCircuits.Add(newCircuit);
                //Console.WriteLine($"New circuit: ({p1}, {p2})");
            }
            //CASE 2a: ONE POINT IS IN A CIRCUIT, SO TAG THIS ON
            else if (circuitMap.ContainsKey(p1) && !circuitMap.ContainsKey(p2))
            {
                var existingCircuit = circuitMap[p1];
                existingCircuit.Add(p2);
                circuitMap[p2] = existingCircuit;
                //Console.WriteLine($"Tag on {p2} to circuit: {p1}");
            }
            //CASE 2b: ONE POINT IS IN A CIRCUIT, SO TAG THIS ON
            else if (!circuitMap.ContainsKey(p1) && circuitMap.ContainsKey(p2))
            {
                var existingCircuit = circuitMap[p2];
                existingCircuit.Add(p1);
                circuitMap[p1] = existingCircuit;
                //Console.WriteLine($"Tag on {p1} to circuit: {p2}");
            }
            //CASE 3: BOTH POINTS ARE IN CIRCUITS ALREADY, SO WE MUST MERGE THE CIRCUITS
            else
            {
                var circuit1 = circuitMap[p1];
                var circuit2 = circuitMap[p2];

                if (circuit1 != circuit2)
                {
                    //Console.WriteLine($"Merge Circuits {p1} <==> {p2}");
                    //MERGE CIRCUITS
                    foreach (var pointIndex in circuit2)
                    {
                        circuit1.Add(pointIndex);
                        circuitMap[pointIndex] = circuit1;
                    }
                    allCircuits.Remove(circuit2);
                }
                else
                {
                    //Console.WriteLine($"Skipping already connected points: {p1} <==> {p2}");
                }
            }

            if ((allCircuits.Count == 1)&&(allCircuits[0].Count == allPoints.Count))
            {
                //THERE IS ONLY ONE CIRCUIT CONTAINING ALL POINTS
                Console.WriteLine("All points connected.");
                //DisplayCircuits(allCircuits);
                return allPoints[p1].X * allPoints[p2].X;
            }
        }
        return 0;
    }

    private static void DisplayCircuits(List<List<int>> allCircuits)
    {
        foreach (var circuit in allCircuits)
        {
            Console.WriteLine($"    CIRCUITS [{circuit.Count}]: {string.Join(", ", circuit)}");
        }
    }

    private static PriorityQueue<(int, int), double> GetAllDistances(List<Point3d> allPoints)
    {
        int count = allPoints.Count;
        var distanceMatrix = new double[count, count];
        var priorityQueue = new PriorityQueue<(int, int), double>();

        for (int i = 0; i < count; i++)
        {
            for (int j = 0; j < count; j++)
            {
                if (i != j)
                {
                    if (distanceMatrix[i, j] != 0)
                    {
                        continue; //ALREADY CALCULATED
                    }
                    double distance = allPoints[i].DistanceTo(allPoints[j]);
                    priorityQueue.Enqueue((i, j), distance);
                    distanceMatrix[i, j] = distance;
                    distanceMatrix[j, i] = distance;
                }
                else
                {
                    distanceMatrix[i, j] = 0;
                }
            }
        }

        return priorityQueue;
    }

    private List<List<int>> GetLargestCircuits(List<List<int>> circuits, int count)
    {
        return [.. circuits.OrderByDescending(c => c.Count).Take(count)];
    }

    private long CalculateProduct(List<List<int>> circuits)
    {
        long product = 1;
        foreach (var circuit in circuits)
        {
            product *= circuit.Count;
        }
        return product;
    }
}