
using System.IO;

namespace AdventOfCode._2023
{
    public class AoCFilesSupplier : IAoCSupplier
    {
        const string filePath = @"\InputData\";
        public string[] GetPuzzleInput(int year, int day)
        {
            var fileName = $"{filePath}{year}_{day}";
            if (File.Exists(fileName))
                return System.IO.File.ReadAllLines(fileName);
            throw new Exception("Input File Could not be found ;-(");
        }
    }
    }
}
