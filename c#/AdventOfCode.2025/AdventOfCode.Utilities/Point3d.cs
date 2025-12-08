public readonly record struct Point3d(long X, long Y, long Z)
{
    public double DistanceTo(Point3d anotherPoint)
    {
        var dx = anotherPoint.X - X;
        var dy = anotherPoint.Y - Y;
        var dz = anotherPoint.Z - Z;

        return Math.Sqrt(dx * dx + dy * dy + dz * dz);
    }
}
