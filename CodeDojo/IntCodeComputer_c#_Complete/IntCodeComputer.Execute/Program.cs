using IntCodeComputer;

internal class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        var intCodeProgram = Helper.LoadFromFile("..\\..\\..\\InputData\\2019day25.txt");
        new IntCodeComputer.Computer().Execute(intCodeProgram);
    }
}
