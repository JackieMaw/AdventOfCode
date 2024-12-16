namespace AdventOfCode._2024.Tests;
public class Map
{
    HashSet<Point> obstacles;
    public Point start;
    public Point? end;
    int maxX;
    int maxY;

    public Map(HashSet<Point> obstacles, Point start, Point? end, int maxX, int maxY)
    {
        this.obstacles = obstacles;
        this.start = start;
        this.end = end;
        this.maxX = maxX;
        this.maxY = maxY;
    }
 
    public static Map CreateMap(string[] input)
    {
        HashSet<Point> obstacles = [];
        Point? start = null;
        Point? end = null;

        int maxY = input.Length;
        int maxX = input[0].Length;

        for (int y = 0; y < input.Length; y++)
        {
            var inputLine = input[y];
            for (int x = 0; x < inputLine.Length; x++)
            {
                switch (inputLine[x])
                {
                    case '#': obstacles.Add(new Point(x, y));
                    break;
                    
                    case 'S': start = new Point(x, y);
                    break;
                    
                    case 'E': end = new Point(x, y);
                    break;

                    case '.': break;

                    default: throw new Exception($"Unexpected Input: {inputLine[x]}");
                }
            }
        }

        if (!start.HasValue)
        {
            throw new Exception("Didn't find a starting position");
        }

        if (!end.HasValue)
        {
            throw new Exception("Didn't find an ending position");
        }

        return new Map(obstacles, start.Value, end, maxX, maxY);
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