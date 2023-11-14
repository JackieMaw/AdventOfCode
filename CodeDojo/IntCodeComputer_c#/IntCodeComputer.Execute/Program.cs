using IntCodeComputer;

internal class Program
{
    private static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        var program = new int [] {};
        new IntCodeComputer.Computer().Execute(program);
    }
}
