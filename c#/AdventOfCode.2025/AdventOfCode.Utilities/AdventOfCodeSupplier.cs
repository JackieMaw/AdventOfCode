public class AoCFilesSupplier : IAoCSupplier
{
    const string filePath = @"C:\Work\AdventOfCode\c#\AdventOfCode.2025\InputData";
    public string[] GetPuzzleInput(int year, int day, string suffix = "")
    {
        var fileName = $@"{filePath}\Day{day:D2}{suffix}.txt";
        if (File.Exists(fileName))
            return File.ReadAllLines(fileName);
        throw new Exception($"Input File Could not be found: {fileName}");
    }
    public string GetPuzzleInput_SingleLine(int year, int day, string suffix = "")
    {
        var fileName = $@"{filePath}\Day{day:D2}{suffix}.txt";
        if (File.Exists(fileName))
            return File.ReadAllText(fileName);
        throw new Exception($"Input File Could not be found: {fileName}");
    }
}
