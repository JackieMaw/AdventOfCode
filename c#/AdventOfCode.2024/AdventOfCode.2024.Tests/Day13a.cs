using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day013a
{
    private const int day = 13;
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
        var expectedResult = 0;
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
        var clawGames = ParseInput(input);

        long result = clawGames.Sum(game => GetMinimumCost(game));

        return result;
    }

    private List<ClawGame> ParseInput(string[] input)
    {
        List<ClawGame> clawGames = [];

        for (int i = 0; i < input.Length; i+=3)
        {
            var buttonA = ParseButton(input[i]);
            var buttonB = ParseButton(input[i+1]);
            var prizeLocation = ParsePrizeLocation(input[i+2]);
            clawGames.Add(new ClawGame(buttonA,buttonB, prizeLocation));
        }

        return clawGames;
    }

/*
Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176
*/
    private Point ParsePrizeLocation(string inputLine)
    {
        var prizeLocationParts = inputLine.Split(',').Select(x => x.Split('=')[1]).Select(x => Convert.ToInt32(x)).ToList();
        return new Point(prizeLocationParts[0], prizeLocationParts[1]);
    }

    private Button ParseButton(string inputLine)
    {
        var buttonParts = inputLine.Split(',').Select(x => x.Split('+')[1]).Select(x => Convert.ToInt32(x)).ToList();
        return new Button(buttonParts[0], buttonParts[1]);
    }

    private long GetMinimumCost(ClawGame game)
    {
        int costA = 3;
        int costB = 1;
    }

    private record struct Button(int X, int Y);
    private record struct ClawGame(Button A, Button B, Point PrizeLocation);
}
