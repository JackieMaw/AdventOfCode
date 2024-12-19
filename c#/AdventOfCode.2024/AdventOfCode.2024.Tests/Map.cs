namespace AdventOfCode._2024.Tests;
public class Map
{
    HashSet<Point> obstacles;
    int maxX;
    int maxY;

    public Map(HashSet<Point> obstacles, int maxX, int maxY)
    {
        this.obstacles = obstacles;
        this.maxX = maxX;
        this.maxY = maxY;
    }    

    public static Point TurnRight(Point direction)
    {
        if (direction == Point.Up) return Point.Right;
        if (direction == Point.Right) return Point.Down;
        if (direction == Point.Down) return Point.Left;
        if (direction == Point.Left) return Point.Up;
        throw new Exception($"Unexpected Direction: {direction}");
    }

    public Point? Move(Point position, Point direction)
    {
        var possibleMove = new Point(position.X + direction.X, position.Y + direction.Y);
        if (IsPossibleMove(possibleMove)) return possibleMove;
        else return null;
    }
    public IEnumerable<Point> GetNeighbours(Point point)
    {
        return point.GetNeighbours().Where(IsPossibleMove);
    }
    private bool IsPossibleMove(Point possibleMove)
    {
        return IsWithinRange(possibleMove) && !IsObstacle(possibleMove);
    }

    private bool IsObstacle(Point possibleMove)
    {
        return obstacles.Contains(possibleMove);
    }

    private bool IsWithinRange(Point currentPosition)
    {
        return (currentPosition.X >= 0) && (currentPosition.Y >= 0) && (currentPosition.X < maxX) && (currentPosition.Y < maxY);
    }    
}