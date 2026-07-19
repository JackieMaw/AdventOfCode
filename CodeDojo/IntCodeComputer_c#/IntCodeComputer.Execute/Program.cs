using IntCodeComputer;

internal class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        var intCodeProgram = Computer.LoadIntCodeProgram(@"C:\Work\AdventOfCode\Data\2019\input\input_2019_25.txt");
        new IntCodeComputer.Computer().Execute(intCodeProgram);
    }
}
