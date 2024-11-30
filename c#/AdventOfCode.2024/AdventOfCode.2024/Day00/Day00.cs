using NUnit.Framework;

namespace AdventOfCode._2024;

public class Day00
{
    private const int day = 9;
    private const int year = 2021;
    
    [Test]
    public void TestSamples()
    {
        
    }

    
    public void TestSampleInput()
    {
        
    }


    public void TestFullInput()
    {
        
    }


    private long Execute(input)
    {
                    Console.WriteLine("How many passwords are valid according to their policies?");
            var inputs = ReadInput.GetStrings("Input.txt");

            int numberOfValidPasswords = 0;
            foreach (var input in inputs)
            {
                var inputParts = input.Split(':');
                var policy = new Policy(inputParts[0]);
                var password = inputParts[1].Trim();

                var isValid = policy.IsValid(password);
                if (isValid)
                    numberOfValidPasswords++;
            }

            Console.WriteLine($"numberOfValidPasswords: {numberOfValidPasswords}");

            Console.WriteLine("All Done!");
    }
}
