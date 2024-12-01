using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day01a
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
        var expectedResult = 11;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test] 
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 1666427;
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
        Array.Sort(input1);
        Array.Sort(input2);
    
        int sumOfDifferences = 0;
        for (int i = 0; i < input.Length; i++)
        {
            System.Console.WriteLine($"{input2[i]} - {input1[i]}");
            sumOfDifferences += Math.Abs(input2[i] - input1[i]);            
        }

        return sumOfDifferences;
    }
}
