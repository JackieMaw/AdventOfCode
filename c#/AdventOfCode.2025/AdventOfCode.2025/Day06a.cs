public class Day06a
{
    private const int day = 6;
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
        //33210 + 490 + 4243455 + 401 = 4277556.
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 4277556;
        var input = aocSupplier.GetPuzzleInput(year, day, "_sample");
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    [Test]
    public void TestFullInput()
    {
        Console.WriteLine("Testing Full Input...");
        var expectedResult = 6378679666679;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var (numbers, operations) = ParseInput(input);
        
        var result = ApplyOperations(numbers, operations);

        return result;
    }

    private long ApplyOperations(List<long[]> numbers, string[] operations)
    {
        long grandTotal = 0;

        for(int opIndex = 0; opIndex < operations.Length; opIndex++)
        {
            var operation = operations[opIndex];
            var result = operation == "*" ? 1L : 0L;
            foreach (var operands in numbers)
            {
                switch(operation)
                {
                    case "+":
                        result += operands[opIndex];
                        break;
                    case "*":
                        result *= operands[opIndex];
                        break;
                    default:
                        throw new Exception($"Unknown operation: {operation}");
                }
            }
            grandTotal += result;
            Console.WriteLine($"#{opIndex} Result of [{operation}] = {result}, Grand Total = {grandTotal}");
        }

        return grandTotal;
    }

    private (List<long[]> numbers, string[] operations) ParseInput(string[] input)
    {
        var allNumbers = new List<long[]>();
        for(int i = 0; i < input.Length - 1; i++)
        {
            var numberParts = input[i].Split(' ', StringSplitOptions.RemoveEmptyEntries).Select(part => long.Parse(part)).ToArray();
            allNumbers.Add(numberParts);
        }

        var operations = input[^1].Split(' ', StringSplitOptions.RemoveEmptyEntries);

        return (allNumbers, operations);
    }


}