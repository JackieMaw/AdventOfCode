public class InputAssistant
{
    public static int[] GetInts(string filename)
    {
        string[] lines = System.IO.File.ReadAllLines(filename);
        return lines.Select(l => Convert.ToInt32(l)).ToArray();
    }

    public static int[] GetIntsFromSingleLine(string inputLine)
    {
        return inputLine.Split(',').Select(l => Convert.ToInt32(l)).ToArray();
    }

    public static long[] GetLongsFromSingleLine(string inputLine)
    {
        return inputLine.Split(',').Select(l => Convert.ToInt64(l)).ToArray();
    }

    public static char[,] GetCharGrid(string[] lines)
    {
        var inputs = lines.Select(l => l.ToCharArray()).ToArray();

        char[,] charArray = new char[lines.Length, lines[0].Length];

        for (int x = 0; x < lines.Length; x++)
        {
            for (int y = 0; y < lines[0].Length; y++)
            {
                charArray[x, y] = inputs[x][y];
            }
        }

        return charArray;
    }

    public static int[,] GetIntGrid(string[] lines)
    {
        var inputs = lines.Select(l => l.ToCharArray()).ToArray();

        int[,] array = new int[lines[0].Length, lines.Length];

        for (int x = 0; x < lines.Length; x++)
        {
            for (int y = 0; y < lines[0].Length; y++)
            {
                array[x, y] = inputs[y][x] - '0';
            }
        }

        return array;
    }

    public static long[] GetLongs(string filename)
    {
        string[] lines = System.IO.File.ReadAllLines(filename);
        return lines.Select(l => Convert.ToInt64(l)).ToArray();
    }

    public static string[] GetStrings(string filename)
    {
        return System.IO.File.ReadAllLines(filename);
    }
}
