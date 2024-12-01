namespace AdventOfCode._2023;

public class AoCFilesSupplier : IAoCSupplier
{
    const string filePath = @"C:\Work\AdventOfCode\c#\AdventOfCode.2024\AdventOfCode.2024.Tests\InputData";
    public string[] GetPuzzleInput(int year, int day, string suffix = "")
    {
        var fileName = $@"{filePath}\Input_{year}_{day}{suffix}.txt";
        if (File.Exists(fileName))
            return File.ReadAllLines(fileName);
        throw new Exception($"Input File Could not be found: {fileName}");
    }
}
