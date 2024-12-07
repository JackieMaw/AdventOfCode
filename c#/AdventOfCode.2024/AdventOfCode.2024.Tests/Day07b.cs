using AdventOfCode._2023;

namespace AdventOfCode._2024.Tests;

public class Day07b
{
    private const int day = 7;
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
        var expectedResult = 11387;
        var input = aocSupplier.GetPuzzleInput(year, day, "_test");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 20928985450275;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var equations = ParseInput(input);
        var result = equations.Where(e => e.CanBeSatisfied()).Sum(e => e.ExpectedResult);
        return result;
    }

    private List<Equation> ParseInput(string[] input)
    {
        return input.Select(inputLine => new Equation(inputLine)).ToList();
    }

    private class Equation
    {
        public long ExpectedResult;
        public List<long> InputValues;

        public Equation(string inputLine)
        {
            var parts = inputLine.Split(": ");
            ExpectedResult = Convert.ToInt64(parts[0]);
            InputValues = parts[1].Split(' ').Select(l => Convert.ToInt64(l)).ToList();
        }

        public bool CanBeSatisfied()
        {
            var possibleOperations = PossibleOperationsCache.GetPossibleOperations(InputValues.Count - 1);

            foreach (var possibleOperationSet in possibleOperations)
            {
                if (IsSatisfied(possibleOperationSet))
                {
                    return true;
                }
            }

            return false;
        }

        private bool IsSatisfied(List<char> operations)
        {
            long result = InputValues[0];

            int valueIndex = 1;
            foreach (var operation in operations) 
            {
                switch (operation)
                {
                    case '+': result += InputValues[valueIndex];
                    break;
                    case 'x': result *= InputValues[valueIndex];
                    break;
                    case '|': 
                    var numDigits = GetNumDigits(InputValues[valueIndex]);
                    result = (long)((result * Math.Pow(10, numDigits)) + InputValues[valueIndex]);
                    break;
                    default:
                    throw new Exception($"Unexpected Operation: {operation}");
                }

                valueIndex++;
            }

            var isSatisfied = result == ExpectedResult;

            if (isSatisfied)
                Console.WriteLine(GetDisplayString(operations));

            return isSatisfied;
        }

        private string GetDisplayString(List<char> operations)
        {
            var displayString = $"{ExpectedResult} = {InputValues[0]}";
            int valueIndex = 1;
            foreach (var operation in operations) 
            {
                displayString = $"{displayString} {operation} {InputValues[valueIndex]}";
                valueIndex++;
            }
            return displayString;
        }

        private int GetNumDigits(long number)
        {   
            int count = 0;

            while (number != 0)
            {
                number /= 10;
                count++;
            }

            return count;
        }
    }

    private static class PossibleOperationsCache
    {
        private static Dictionary<int, List<List<char>>> _possibleOperations = [];

        public static List<List<char>> GetPossibleOperations(int numOperations)
        {
            if (_possibleOperations.TryGetValue(numOperations, out var possibleOperations))
            {
                return possibleOperations;
            }
            else
            {
                var newPossibleOperations = PermutationGenerator<char>.GetPermutations(['x', '+', '|'], numOperations);
                _possibleOperations[numOperations] = newPossibleOperations;
                return newPossibleOperations;
            }
        }
    }
}
