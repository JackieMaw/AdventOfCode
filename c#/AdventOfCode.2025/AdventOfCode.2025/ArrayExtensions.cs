using System.Linq;

public static class ArrayExtensions
{
    public static bool TrySetValue<T>(this T[][] array, T value, int row, int col)
    {
        if (array == null)
            return false;
        if (row < 0 || row >= array.Length)
            return false;
        var rowArr = array[row];
        if (rowArr == null)
            return false;
        if (col < 0 || col >= rowArr.Length)
            return false;
        rowArr[col] = value;
        return true;
    }

    public static bool TrySetValue<T>(this T[,] array, T value, int row, int col)
    {
        if (array == null)
            return false;
        if (row < 0 || row >= array.GetLength(0))
            return false;
        if (col < 0 || col >= array.GetLength(1))
            return false;
        array[row, col] = value;
        return true;
    }

    public static char[,] ToCharArray2D(this string[] input)
    {
        if (input == null || input.Length == 0)
            return new char[0, 0];

        int rows = input.Length;
        int cols = input.Max(s => s?.Length ?? 0);
        var result = new char[rows, cols];

        for (int r = 0; r < rows; r++)
        {
            var line = input[r] ?? string.Empty;
            for (int c = 0; c < cols; c++)
            {
                result[r, c] = c < line.Length ? line[c] : '\0';
            }
        }

        return result;
    }
}
