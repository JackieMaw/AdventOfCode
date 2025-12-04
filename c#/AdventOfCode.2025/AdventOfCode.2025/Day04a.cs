[TestFixture]
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
        var expectedResult = 13;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 1411;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        long howManyPaperRollsCollected = 0;

        int width = input[0].Length;
        int length = input.Length;

        for (int x = 0; x < length; x++)
        {
            for (int y = 0; y < width; y++)
            {
                char currentChar = input[x][y];

                if (currentChar == '@')
                {
                    //can we pick up this roll of paper?
                    //how many adjacent rolls of paper are there?
                    int adjacentCount = CountAdjacentPaperRolls(input, x, y, length, width);
                    if (adjacentCount < 4)
                    {
                        howManyPaperRollsCollected++;
                        Console.Write("X");
                    }
                    else
                    {
                        Console.Write("@");
                    }
                }
                else
                {
                    Console.Write(currentChar);
                }
            }
            Console.WriteLine();
        }

        return howManyPaperRollsCollected;
    }

    private int CountAdjacentPaperRolls(string[] input, int x, int y, int length, int width)
    {
        var countOfAdjacentPaperRolls = 0;

        var directions = new int[8][]
        {
            [-1, 0], // Up
            [1, 0],  // Down
            [0, -1], // Left
            [0, 1],   // Right

            //diagonals
            [-1, -1], // Top Left
            [-1, 1],  // Top Right
            [1, -1], // Botton Left
            [1, 1]   // Botton Right
        };

        foreach (var direction in directions)
        {
            int newX = x + direction[0];
            int newY = y + direction[1];

            if (IsValidPosition(length, width, newX, newY))
            {
                if (input[newX][newY] == '@')
                {
                    //found adjacent roll of paper
                    countOfAdjacentPaperRolls++;
                }
            }
        }

        return countOfAdjacentPaperRolls;
    }

    private static bool IsValidPosition(int length, int width, int newX, int newY)
    {
        return newX >= 0 && newX < length && newY >= 0 && newY < width;
    }
}