public class Day06b
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
        //4 + 431 + 623 = 1058
        //1058 + 3253600 + 625 + 8544 = 3263827.
        Console.WriteLine("Testing Sample Input...");
        var expectedResult = 3263827;
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

    private long ApplyOperations(List<string[]> numbers, string[] operations)
    {
        long grandTotal = 0;

        for(int opIndex = 0; opIndex < operations.Length; opIndex++)
        {
            var collectedNumbers = CollectNumbers(numbers, opIndex);
            var operation = operations[opIndex];
            long result = ApplyOperation(collectedNumbers, operation);
            grandTotal += result;
            Console.WriteLine($"#{opIndex} Result of [{operation}] = {result}, Grand Total = {grandTotal}");
        }

        return grandTotal;
    }

    private static long ApplyOperation(List<long> collectedNumbers, string operation)
    {
        var result = operation == "*" ? 1L : 0L;
        foreach (var operand in collectedNumbers)
        {
            switch (operation)
            {
                case "+":
                    result += operand;
                    break;
                case "*":
                    result *= operand;
                    break;
                default:
                    throw new Exception($"Unknown operation: {operation}");
            }
        }

        return result;
    }

    private List<long> CollectNumbers(List<string[]> numbers, int opIndex)
    {
        bool stillMoreNumbersToCollect = true;
        int numberIndex = -1;
        var collectedNumbers = new List<long>();

        while (stillMoreNumbersToCollect)
        {
            numberIndex++;
            long accumulatedValue = 0L;
            foreach (var operands in numbers)
            {
                var operand = operands[opIndex];
                if (numberIndex < operand.Length)
                {
                    int thisValue = int.Parse(operand[numberIndex].ToString());
                    if (accumulatedValue == 0L)
                    {
                        accumulatedValue = thisValue;
                    }
                    else
                    {
                        accumulatedValue *= 10;
                        accumulatedValue += thisValue;
                    }
                }
            }
            if (accumulatedValue == 0L)
            {
                stillMoreNumbersToCollect = false;
            }
            else
            {
                collectedNumbers.Add(accumulatedValue);                
            }
        }

        return collectedNumbers;
    }

    private (List<string[]> numbers, string[] operations) ParseInput(string[] input)
    {
        var allNumbers = new List<string[]>();
        for(int i = 0; i < input.Length - 1; i++)
        {
            var numberParts = input[i].Split(' ', StringSplitOptions.RemoveEmptyEntries);
            allNumbers.Add(numberParts);
        }

        var operations = input[^1].Split(' ', StringSplitOptions.RemoveEmptyEntries);

        return (allNumbers, operations);
    }


}