public readonly record struct Point(long X, long Y)
{
    public static Point Up = new(0, -1);
    public static Point Right = new(1, 0);
    public static Point Down = new(0, 1);
    public static Point Left = new(-1, 0);

    public IEnumerable<Point> GetNeighbours()
    {
        var allDirections = new List<Point> {Up, Right, Down, Left};
        var thisPoint = this;
        return allDirections.Select(thisPoint.Move);
    }

    public Point Move(Point direction)
    {
        return new Point(X + direction.X, Y + direction.Y);
    }
}
