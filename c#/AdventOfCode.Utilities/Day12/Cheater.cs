using System;
using System.Collections.Generic;
using System.IO;

namespace Day12
{
    public static class Cheater
    {
        public static int SolvePuzzle1(string[] routeLines)
        {
            Dictionary<char, double> directionAngles = new Dictionary<char, double>()
            {
                { 'N', Math.PI / -2d },
                { 'S', Math.PI / 2d },
                { 'E', 0 },
                { 'W', Math.PI },
            };

            Dictionary<char, double> degreeToRad = new Dictionary<char, double>()
            {
                { 'L', Math.PI / -180 },
                { 'R', Math.PI / 180 },
            };

            (double x, double y) pos = (0d, 0d);
            var direction = 0d;

            static (double x, double y) AddVector((double x, double y) start, double angle, double length) =>
                (length * Math.Cos(angle) + start.x, length * Math.Sin(angle) + start.y);

            foreach (var move in routeLines)
            {
                var arg = double.Parse(move[1..]);
                if (directionAngles.TryGetValue(move[0], out var movementAngle))
                {
                    pos = AddVector(pos, movementAngle, arg);
                }
                else if (degreeToRad.TryGetValue(move[0], out var rotationAngle))
                {
                    direction += arg * rotationAngle;
                }
                else
                {
                    pos = AddVector(pos, direction, arg);
                }

                Console.WriteLine($"Ship is here: ({Math.Round(pos.x)},{Math.Round(pos.y)}), facing direction {direction}");

            }

            return Math.Abs((int)Math.Round(pos.x, 0)) + Math.Abs((int)Math.Round(pos.y, 0));
        }

        public static long SolvePuzzle2(string[] routeLines)
        {
            (double x, double y) pos = (0d, 0d);
            (double x, double y) waypoint = (10d, -1d);

            static (double x, double y) RotateVector((double x, double y) start, double angle) =>
                (Math.Cos(angle) * start.x - Math.Sin(angle) * start.y, Math.Sin(angle) * start.x + Math.Cos(angle) * start.y);

            Console.WriteLine($"Ship is here: ({Math.Round(pos.x)},{Math.Round(pos.y)}), Waypoint is here ({Math.Round(waypoint.x)},{Math.Round(waypoint.y)})");

            foreach (var move in routeLines)
            {
                var arg = double.Parse(move[1..]);
                switch (move[0])
                {
                    case 'N':
                        waypoint = (waypoint.x, waypoint.y + arg * -1);
                        break;
                    case 'S':
                        waypoint = (waypoint.x, waypoint.y + arg);
                        break;
                    case 'E':
                        waypoint = (waypoint.x + arg, waypoint.y);
                        break;
                    case 'W':
                        waypoint = (waypoint.x + arg * -1, waypoint.y);
                        break;
                    case 'F':
                        pos = (pos.x + waypoint.x * arg, pos.y + waypoint.y * arg);
                        break;
                    case 'R':
                        waypoint = RotateVector(waypoint, arg * Math.PI / 180);
                        break;
                    case 'L':
                        waypoint = RotateVector(waypoint, arg * Math.PI / -180);
                        break;
                }

                Console.WriteLine($"Ship is here: ({Math.Round(pos.x)},{Math.Round(pos.y)}), Waypoint is here ({Math.Round(waypoint.x)},{Math.Round(waypoint.y)})");
            }

            return Math.Abs((int)Math.Round(pos.x, 0)) + Math.Abs((int)Math.Round(pos.y, 0));
        }
    }
}