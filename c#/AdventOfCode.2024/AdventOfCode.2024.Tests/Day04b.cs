using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day04b
{
    private const int day = 4;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    } 

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 9;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test]
    public void TestSampleInput2()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 0;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test2");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 2005;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    private long Execute(string[] input)
    {
        var charArray = ReadInput.GetChars(input);
        var count = 0;
        for (int i = 0; i < charArray.GetLength(0); i++) 
        {
            for (int j = 0; j < charArray.GetLength(1); j++) 
            {
                if (charArray[i, j] == 'A')
                {
                    if (SearchForMasXAtPosition(charArray, i, j))
                        count += 1;
                }
            }
        }
        return count;
    }

    private bool SearchForMasXAtPosition(char[,] charArray, int i, int j)
    {
        var diagonal1 = new[] { (-1, -1), (1,1) };
        var diagonal2 = new[] { (-1,1), (1, -1) };
        
        return (CheckDiagonal(charArray, i, j, diagonal1) && CheckDiagonal(charArray, i, j, diagonal2));
    }

    private bool CheckDiagonal(char[,] charArray, int i, int j, (int, int)[] diagonal)
    {
       var char1 = GetCharByOffset(charArray, i, j, diagonal[0]);
       var char2 = GetCharByOffset(charArray, i, j, diagonal[1]);

       if (char1 is null) return false;
       if (char2 is null) return false;

       if ((char1 == 'M' && char2 == 'S') || (char1 == 'S' && char2 == 'M')) return true;

       return false;       
    }

    private char? GetCharByOffset(char[,] charArray, int i, int j, (int, int) offset)
    { 
        var i2 = i + offset.Item1;
        var j2 = j + offset.Item2;

        // if in range, check for the next letter
        if (IsIndexInRange(charArray, i2, j2))
            return charArray[i2, j2];
        
        return null;
    }

    private bool CheckDirection(char[,] charArray, int i, int j, string toFind, (int, int) direction)
    {
        for (int k = 0; k < toFind.Length; k++)
        {
            var charToFind = toFind[k];

            var i2 = i + (direction.Item1 * (k + 1));
            var j2 = j + (direction.Item2 * (k + 1));

            // if in range, check for the next letter
            if (IsIndexInRange(charArray, i2, j2))
            {
                if (charArray[i2, j2] != charToFind)
                {
                    return false;
                }
            }
            else
            {
                return false;
            }
        }

        System.Console.WriteLine($"Found XMAS at Position ({i},{j}) in direction {direction}");
        return true;
    }

    public bool IsIndexInRange(char[,] array, int row, int col)
    {
        int rows = array.GetLength(0);
        int cols = array.GetLength(1);

        return row >= 0 && row < rows && col >= 0 && col < cols;
    }
}
