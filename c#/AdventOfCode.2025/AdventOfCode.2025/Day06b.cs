public class Day06b
{
    private const int day = 6;
    private const int year = 2024;
    private IAoCSupplier aocSupplier = new AoCFilesSupplier();

    [SetUp]
    public void Setup()
    {
    }

    /*
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
Reading the problems right-to-left one column at a time, the problems are now quite different:

The rightmost problem is 4 + 431 + 623 = 1058
The second problem from the right is 175 * 581 * 32 = 3253600
The third problem from the right is 8 + 248 + 369 = 625
Finally, the leftmost problem is 356 * 24 * 1 = 8544
    */

    [Test]
    public void CanParseInputWithSpacesOnLeft()
    {
        var input = new string[]
        {
            "123",
            " 45",
            "  6",
            "*"
        };

        var allOperationInfo = ParseInput(input);
        Assert.That(allOperationInfo, Has.Exactly(1).Items);

        var operationInfo = allOperationInfo[0];
        Assert.That(operationInfo.NumberStrings, Has.Exactly(3).Items);
        Assert.That(operationInfo.NumberStrings[0], Is.EqualTo("123"));
        Assert.That(operationInfo.NumberStrings[1], Is.EqualTo(" 45"));
        Assert.That(operationInfo.NumberStrings[2], Is.EqualTo("  6"));
    }

    
    [Test]
    public void CanParseInputWithSpacesOnRight()
    {
        var input = new string[]
        {
            "64",
            "23",
            "314",
            "+"
        };

        var allOperationInfo = ParseInput(input);
        Assert.That(allOperationInfo, Has.Exactly(1).Items);

        var operationInfo = allOperationInfo[0];
        Assert.That(operationInfo.NumberStrings, Has.Exactly(3).Items);
        Assert.That(operationInfo.NumberStrings[0], Is.EqualTo("64"));
        Assert.That(operationInfo.NumberStrings[1], Is.EqualTo("23"));
        Assert.That(operationInfo.NumberStrings[2], Is.EqualTo("314"));
    }

    [Test]
    public void CanCollectNumbersWithSpacesOnRight()
    {
        List<string> numberStrings = 
        [
            "64",
            "23",
            "314",
        ];

        var numbers = CollectNumbers(numberStrings);
        Assert.That(numbers, Has.Exactly(3).Items);

        Assert.That(numbers[0], Is.EqualTo(623));
        Assert.That(numbers[1], Is.EqualTo(431));
        Assert.That(numbers[2], Is.EqualTo(4));
    }

    [Test]
    public void CanCollectNumbersWithSpacesOnLeft()
    {
        List<string> numberStrings = 
        [
            "123",
            " 45",
            "  6"
        ];

        var numbers = CollectNumbers(numberStrings);
        Assert.That(numbers, Has.Exactly(3).Items);

        Assert.That(numbers[0], Is.EqualTo(1));
        Assert.That(numbers[1], Is.EqualTo(24));
        Assert.That(numbers[2], Is.EqualTo(356));
    }

    [Test]
    public void CanHandleSpacesOnLeft()
    {
        var input = new string[]
        {
            "123",
            " 45",
            "  6",
            "*"
        };

        var result = Execute(input);
        var expectedResult = 8544;
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    
    [Test]
    public void CanHandleSpacesOnRight()
    {
        var input = new string[]
        {
            "64",
            "23",
            "314",
            "+"
        };


        var result = Execute(input);
        var expectedResult = 1058;
        Assert.That(result, Is.EqualTo(expectedResult));
    }    

    [Test]
    public void TestSampleInput()
    {
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
        var expectedResult = 11494432585168;
        var input = aocSupplier.GetPuzzleInput(year, day);
        var result = Execute(input);
        Console.WriteLine($"Result: {result}");
        Assert.That(result, Is.EqualTo(expectedResult));
    }

    private long Execute(string[] input)
    {
        var allOperationInfo = ParseInput(input);
        
        var result = ApplyOperations(allOperationInfo);

        return result;
    }

    private long ApplyOperations(List<OperationInfo> allOperationInfo)
    {
        long grandTotal = 0;

        foreach (var operationInfo in allOperationInfo)
        {
            Console.WriteLine($"Operation: {operationInfo.Operation}, Numbers: '{string.Join("', '", operationInfo.NumberStrings)}'");
            var collectedNumbers = CollectNumbers(operationInfo.NumberStrings);
            long result = ApplyOperation(collectedNumbers, operationInfo.Operation);
            grandTotal += result;
            Console.WriteLine($"Result of [{operationInfo.Operation}] = {result}, Grand Total = {grandTotal}");
        }

        return grandTotal;
    }

    private static long ApplyOperation(List<long> collectedNumbers, char operation)
    {
        var result = operation == '*' ? 1L : 0L;
        foreach (var operand in collectedNumbers)
        {
            switch (operation)
            {
                case '+':
                    result += operand;
                    break;
                case '*':
                    result *= operand;
                    break;
                default:
                    throw new Exception($"Unknown operation: {operation}");
            }
        }

        return result;
    }

    private List<long> CollectNumbers(List<string> numberStrings)
    {
        int maxLength = numberStrings.Max(ns => ns.Length);

        var collectedNumbers = new List<long>();

        for (int numberIndex = 0; numberIndex < maxLength; numberIndex++)
        {
            long accumulatedValue = 0L;
            foreach (var numberString in numberStrings)
            {
                if (numberIndex < numberString.Length)
                {
                    char thisDigit = numberString[numberIndex];
                    if (thisDigit != ' ')
                    {
                        int thisValue = int.Parse(thisDigit.ToString());
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
            }
            collectedNumbers.Add(accumulatedValue);      
        }

        return collectedNumbers;
    }

    private List<OperationInfo> ParseInput(string[] input)
    {
        List<OperationInfo> allOperationInfo = ParseOperations(input[^1]);
        ParseNumberStrings(input, allOperationInfo);
        return allOperationInfo;
    }

    private static void ParseNumberStrings(string[] input, List<OperationInfo> allOperationInfo)
    {
        foreach (var operationInfo in allOperationInfo)
        {
            for (int i = 0; i < input.Length - 1; i++)
            {
                var inputLine = input[i];
                if (operationInfo.EndsAt == -1)
                {
                    var numberString = inputLine.Substring(operationInfo.StartsAt);
                    operationInfo.NumberStrings.Add(numberString);
                }
                else
                {
                    var numberString = inputLine.Substring(operationInfo.StartsAt, operationInfo.EndsAt - operationInfo.StartsAt);
                    operationInfo.NumberStrings.Add(numberString);
                }
                
            }
        }
    }

    private static List<OperationInfo> ParseOperations(string operationalLine)
    {
        var operations = new List<OperationInfo>();
        OperationInfo? operationInfo = null;
        for (int i = 0; i < operationalLine.Length; i++)
        {
            var ch = operationalLine[i];
            if (ch != ' ')
            {
                if (operationInfo == null)
                {
                    operationInfo = new OperationInfo(ch, i);
                }
                else
                {
                    operationInfo.EndsAt = i - 1;
                    operations.Add(operationInfo);
                    operationInfo = new OperationInfo(ch, i);
                }
            }
        }
        operations.Add(operationInfo);
        return operations;
    }

    private class OperationInfo
    {
        public OperationInfo(char operation, int startsAt)
        {
            Operation = operation;
            StartsAt = startsAt;
            EndsAt = -1;
            NumberStrings = [];
        }

        public char Operation { get; internal set; }
        public int StartsAt { get; internal set; }
        public int EndsAt { get; internal set; }
        public List<string> NumberStrings { get; internal set;  }
    }
}
