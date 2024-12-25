using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day25
{
    private const int day = 25;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void UnitTests()
    {
        Assert.That(DoesKeyFitLock([0,5,3,4,3], [5,0,2,1,3]), Is.EqualTo(false));
        Assert.That(DoesKeyFitLock([0,5,3,4,2], [5,0,2,1,3]), Is.EqualTo(true));
    }    

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 3;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 0;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {        
        var (keys, locks) = ParseInput(input);
        int countFits = 0;

        foreach (var k in keys)
            foreach (var l in locks)
            {
                if (DoesKeyFitLock(k, l))
                    countFits++;
            }

        return countFits;
    }

    private (List<int[]> keys, List<int[]> locks) ParseInput(string[] input)
    {
        List<int[]> keys = [];
        List<int[]> locks = [];

        for (int i = 0; i < input.Length; i+=8)
        {
            var chunk = input.Skip(i).Take(7).ToList();

            if (chunk[0] == ".....")
            {
                var key = ParseKey(chunk);
                keys.Add(key);
            }
            else if (chunk[0] == "#####")
            {
                var l = ParseLock(chunk);
                locks.Add(l);
            }
        }

        return (keys, locks);
    }

    private static int[] ParseKey(List<string> chunk)
    {
        int[] key = new int[chunk[0].Length];
        //counting from bottom up
        //counting from top down
        for (int r = 6; r > 0; r--)
        {
            var thisLine = chunk[r];
            for (int c = 0; c < thisLine.Length; c++)
            {
                if (thisLine[c] == '#')
                {
                    key[c] = 6 - r;
                }
            }
        }
        return key;
    }

    private static int[] ParseLock(List<string> chunk)
    {
        int[] key = new int[chunk[0].Length];
        //counting from top down
        for (int r = 0; r < 6; r++)
        {
            var thisLine = chunk[r];
            for (int c = 0; c < thisLine.Length; c++)
            {
                if (thisLine[c] == '#')
                {
                    key[c] = r;
                }
            }
        }
        return key;
    }

    private bool DoesKeyFitLock(int[] k, int[] l)
    {       
        for (int c = 0; c < k.Length; c++)
        {
            if (k[c] + l[c] > 5)
            {
                System.Console.WriteLine($"Lock {string.Join(",", l)} and key {string.Join(",", k)} do not fit.");
                return false;
            }
        }


        System.Console.WriteLine($"Lock {string.Join(",", l)} and key {string.Join(",", k)} fit perfectly!");
        return true;
    }
}
