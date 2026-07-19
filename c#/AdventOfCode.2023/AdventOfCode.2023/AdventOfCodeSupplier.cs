
using System.IO;

namespace AdventOfCode._2023
{
    public class AoCFilesSupplier : IAoCSupplier
    {
        const string filePath = @"C:\Work\AdventOfCode\Data";
        public string[] GetPuzzleInput(int year, int day)
        {
            var fileName = $@"{filePath}\{year}\input\input_{year}_{day}.txt";
            if (File.Exists(fileName))
                return System.IO.File.ReadAllLines(fileName);
            throw new Exception("Input File Could not be found ;-(");
        }
    }
    }
}
