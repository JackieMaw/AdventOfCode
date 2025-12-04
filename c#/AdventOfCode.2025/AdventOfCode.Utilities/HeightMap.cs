public class HeightMap
{
    public int[,] Heights;

    public HeightMap(int[,] heights)
    {
        Heights = heights;
    }    

    public int GetHeight(Point point)
    {
        return Heights[point.X, point.Y];
    }

    public IEnumerable<Point> GetNeighbours(Point point)
    {
        return point.GetNeighbours().Where(IsWithinRange);
    }

    private bool IsWithinRange(Point point)
    {
        return (point.X >= 0) && (point.Y >= 0) && (point.X < Heights.GetLength(0)) && (point.Y < Heights.GetLength(1));
    }    
}
