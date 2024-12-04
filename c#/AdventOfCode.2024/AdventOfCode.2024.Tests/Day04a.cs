using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day04a
{
    private const int day = 4;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    [Test]
    public void TestCheckDirectionForwards()
    {
        var charArray = ReadInput.GetChars(["XMAS", "    ", "    "]);
        var found = CheckDirection(charArray, 0, 0, "MAS", (0, 1));
        Assert.That(found, Is.EqualTo(true));        
    } 

    [Test]
    public void TestSearchForXmasAtPositionForwards()
    {
        var charArray = ReadInput.GetChars(["XMAS", "    ", "    "]);
        var numFound = SearchForXmasAtPosition(charArray, 0, 0);
        Assert.That(numFound, Is.EqualTo(1));        
    } 

    [Test]
    public void TestExecuteForwards()
    {
        Assert.That(Execute(["XMAS", "    ", "    "]), Is.EqualTo(1));        
    }   

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 4;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(expectedResult, Is.EqualTo(result));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 2639;
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
                if (charArray[i, j] == 'X')
                {
                    count += SearchForXmasAtPosition(charArray, i, j);
                }
            }
        }
        return count;
    }

    private int SearchForXmasAtPosition(char[,] charArray, int i, int j)
    {
        var directions = new[] { (-1, -1), (-1, 0), (-1,1), (0, -1), (0,1), (1, -1), (1, 0), (1,1), };
        var toFind = "MAS";
        var numFound = 0;

        foreach (var direction in directions)
        {
            if (CheckDirection(charArray, i, j, toFind, direction))
            {
                numFound++;
            }
        }
        return numFound;
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
