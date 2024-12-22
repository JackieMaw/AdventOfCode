using System.Security.Cryptography.X509Certificates;
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
    public void UnitTest_TestCase1()
    {
        Console.WriteLine("Testing Case 1...");
        var expectedResult = 280;
        var input = new string [] { "Button A: X+94, Y+34", "Button B: X+22, Y+67", "Prize: X=8400, Y=5400" };
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }    

    [Test]
    public void UnitTest_TestCase2()
    {
        Console.WriteLine("Testing Case 2...");
        var expectedResult = 0;
        var input = new string [] { "Button A: X+26, Y+66", "Button B: X+67, Y+21", "Prize: X=12748, Y=12176" };
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    } 

    [Test]
    public void TestSampleInput()
    {
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 480;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 29201;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var clawGames = ParseInput(input);

        long result = clawGames.Sum(GetMinimumCost);

        return result;
    }

    private List<ClawGame> ParseInput(string[] input)
    {
        List<ClawGame> clawGames = [];

        for (int i = 0; i < input.Length; i+=4)
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

    private int GetMinimumCost_Dumb(ClawGame game)
    {
        int costA = 3;
        int costB = 1;
        
        int? lowestCost = null;

        System.Console.WriteLine($"{game}");

        for (int a = 100; a >= 0; a--)
        {
            double b = (game.PrizeLocation.X - (game.ButtonA.X * a))/(double)game.ButtonB.X;
            if (((b % 1) == 0) && (b >= 0) && (b <= 100))
            {
                int totalCost = costA * a + costB * (int)b;
                System.Console.WriteLine($"    {a}x{costA} + {b}x{costB} = {totalCost}");

                if (!lowestCost.HasValue)
                {
                    lowestCost = totalCost;
                }
                else if (totalCost < lowestCost.Value)
                {
                    lowestCost = totalCost;
                }
            }
        }

        return lowestCost ?? 0;
    }

    private long GetMinimumCost(ClawGame game)
    {
        int costA = 3;
        int costB = 1;

        double top = game.PrizeLocation.X * game.ButtonA.Y - game.PrizeLocation.Y * game.ButtonA.X;
        double bottom = game.ButtonB.X * game.ButtonA.Y - game.ButtonA.X * game.ButtonB.Y;
        double B = top / bottom;
        double A = (game.PrizeLocation.X - game.ButtonB.X * B) / game.ButtonA.X;

        if (IsValidPlay(A) && IsValidPlay(B))
        {
            return costA * (int)A + costB * (int)B;
        }
        else
        {
            return 0;
        }
    }

    private static bool IsValidPlay(double numClicks)
    {
        return ((numClicks % 1) == 0) && (numClicks >= 0) && (numClicks <= 100);
    }

    private record struct Button(int X, int Y);
    private record struct ClawGame(Button ButtonA, Button ButtonB, Point PrizeLocation);
}
