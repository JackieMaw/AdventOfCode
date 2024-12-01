using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day01b
{
    private const int day = 1;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void UnitTests()
    {
        Assert.Pass();
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 31;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test] 
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 24316233;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    private Tuple<int[], int[]> SplitPuzzleInput(string [] input)
    {
        int[] input1 = new int[input.Length];
        int[] input2 = new int[input.Length];

        for (int i = 0; i < input.Length; i++)
        {
            var inputPair = input[i].Split(' ', StringSplitOptions.RemoveEmptyEntries);
            input1[i] = Convert.ToInt32(inputPair[0]);
            input2[i] = Convert.ToInt32(inputPair[1]);
        }
        return Tuple.Create(input1, input2);
    }

    private long Execute(string[] input)
    {
        Array.ForEach(input, Console.WriteLine);
        var splitInput = SplitPuzzleInput(input);
        var input1 = splitInput.Item1;
        var input2 = splitInput.Item2;

        Dictionary<int, int> hashCount1 = GetHashCount(input1);
        Dictionary<int, int> hashCount2 = GetHashCount(input2);

        int sumOfSimilarityScore = 0;
        foreach (var keyValuePair in hashCount1)
        {
            if (hashCount2.ContainsKey(keyValuePair.Key))
            {
                var similarityScore = keyValuePair.Key * keyValuePair.Value * hashCount2[keyValuePair.Key];
                sumOfSimilarityScore += similarityScore;
            }
        }

        return sumOfSimilarityScore;
    }

    private static Dictionary<int, int> GetHashCount(int[] input1)
    {
        var hashCount1 = new Dictionary<int, int>();
        foreach (var i in input1)
        {
            if (hashCount1.ContainsKey(i))
            {
                hashCount1[i] += 1;
            }
            else
            {
                hashCount1[i] = 1;
            }
        }

        return hashCount1;
    }
}
