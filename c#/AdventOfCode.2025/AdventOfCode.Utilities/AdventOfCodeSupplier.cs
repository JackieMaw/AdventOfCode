public class AoCFilesSupplier : IAoCSupplier
{
    const string filePath = @"C:\Work\AdventOfCode\Data";
    public string[] GetPuzzleInput(int year, int day, string suffix = "")
    {
        suffix = suffix == "_sample" ? "_test" : suffix;
        var fileName = $@"{filePath}\{year}\input\input_{year}_{day}{suffix}.txt";
        if (File.Exists(fileName))
            return File.ReadAllLines(fileName);
        throw new Exception($"Input File Could not be found: {fileName}");
    }
    public string GetPuzzleInput_SingleLine(int year, int day, string suffix = "")
    {
        suffix = suffix == "_sample" ? "_test" : suffix;
        var fileName = $@"{filePath}\{year}\input\input_{year}_{day}{suffix}.txt";
        if (File.Exists(fileName))
            return File.ReadAllText(fileName);
        throw new Exception($"Input File Could not be found: {fileName}");
    }
}
