
namespace IntCodeComputer
{
    public static class Helper
    {
        public static long[] LoadFromFile(string filePath)
        {
            return LoadFromString(System.IO.File.ReadAllLines(filePath)[0]);
        }

        public static long[] LoadFromString(string inputData)
        {
            return inputData.Split(',').Select(l => Convert.ToInt64(l)).ToArray();
        }
    }
}