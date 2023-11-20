
namespace IntCodeComputer
{
    public static class Helper
    {
        public static int[] LoadIntsFromFile(string filePath)
        {
            return GetIntsFromString(System.IO.File.ReadAllLines(filePath)[0]);
        }

        public static int[] GetIntsFromString(string inputData)
        {
            return inputData.Split(',').Select(l => Convert.ToInt32(l)).ToArray();
        }
    }
}