using System;

namespace Day12
{
    internal class Turtle
    {
        //relative to the ship's starting point
        int shipX;
        int shipY;

        enum Direction
        {
            North, East, South, West
        }

        int direction = 90; //ship starts facing east

        //relative to the ship
        int waypointX; 
        int waypointY;

        public Turtle(int x, int y)
        {
            this.waypointX = x;
            this.waypointY = y;
        }

        internal void MoveWaypoint(string i)
        {
            /*
            Action N means to move north by the given value.
            Action S means to move south by the given value.
            Action E means to move east by the given value.
            Action W means to move west by the given value.
            Action L means to turn left the given number of degrees.
            Action R means to turn right the given number of degrees.
            Action F means to move forward by the given value in the direction the ship is currently facing.
            */

            char action = i[0];
            int distance = Convert.ToInt32(i.Substring(1));

            switch (action) 
            {
                case 'N':
                    Console.Write($"Move Waypoint North by {distance}");
                    waypointY += distance;
                    break;
                case 'S':
                    Console.Write($"Move Waypoint South by {distance}");
                    waypointY -= distance;
                    break;
                case 'E':
                    Console.Write($"Move Waypoint East by {distance}");
                    waypointX += distance;
                    break;
                case 'W':
                    Console.Write($"Move Waypoint West by {distance}");
                    waypointX -= distance;
                    break;
                case 'L':
                    Console.Write($"Rotate Waypoint Left by {distance}");
                    Rotate(-distance);
                    break;
                case 'R':
                    Console.Write($"Rotate Waypoint Right by {distance}");
                    Rotate(+distance);
                    break;
                case 'F':
                    Console.Write($"Move Ship Towards Waypoint by {distance}");
                    MoveShipTowardsWaypoint(distance);
                    break;

                default:
                    Console.WriteLine($"INSTRUCTION NOT SUPPORTED");
                    break;
            }

            Console.Write($" ==> Ship is here: ({shipX},{shipY}), facing direction {direction}");
            Console.WriteLine($" ==> Waypoint is here: ({waypointX},{waypointY})");
        }

        private void MoveShipTowardsWaypoint(int distance)
        {
            //ship moves, waypoint stays relative distance away
            shipX += waypointX * distance;
            shipY += waypointY * distance;
        }

        private void Rotate(int degreesToRotate)
        {
            if (degreesToRotate < 0)
                degreesToRotate += 360;

            for (int i = 0; i < degreesToRotate / 90; i++)
            {
                RotateBy90ToTheRight();
            }   
        }

        private void RotateBy90ToTheRight()
        {
            int X = Math.Abs(waypointX);
            int Y = Math.Abs(waypointY);

            
            if (waypointX >= 0 && waypointY >= 0) //Quadrant 1
            {
                waypointY = -X;
                waypointX = Y;
            }
            else if (waypointX >= 0 && waypointY <= 0) //Quadrant 2 (y is -ve)
            {
                waypointY = -X;
                waypointX = -Y;
            }
            else if (waypointX <= 0 && waypointY <= 0) //Quadrant 3 (both x and y is -ve)
            {
                waypointY = X;
                waypointX = -Y;
            }
            else if (waypointX <= 0 && waypointY >= 0) //Quadrant 4 (x -ve)
            {
                waypointY = X;
                waypointX = Y;
            }
        }

        internal void MoveShip(string i)
        {
            /*
            Action N means to move north by the given value.
            Action S means to move south by the given value.
            Action E means to move east by the given value.
            Action W means to move west by the given value.
            Action L means to turn left the given number of degrees.
            Action R means to turn right the given number of degrees.
            Action F means to move forward by the given value in the direction the ship is currently facing.
            */

            char action = i[0];
            int distance = Convert.ToInt32(i.Substring(1));

            switch (action)
            {
                case 'N': 
                    Console.Write($"Move North by {distance}");
                    shipY += distance;
                    break;
                case 'S':
                    Console.Write($"Move South by {distance}");
                    shipY -= distance;
                    break;
                case 'E':
                    Console.Write($"Move East by {distance}");
                    shipX += distance;
                    break;
                case 'W':
                    Console.Write($"Move West by {distance}");
                    shipX -= distance;
                    break;
                case 'L':
                    Console.Write($"Turn Left by {distance}");
                    direction -= distance;
                    direction = direction % 360;
                    break;
                case 'R':
                    Console.Write($"Turn Right by {distance}");
                    direction += distance;
                    direction = direction % 360;
                    break;
                case 'F':
                    Console.Write($"Move Forward by {distance}");
                    MoveForward(distance);
                    break;

                default:
                    Console.WriteLine($"INSTRUCTION NOT SUPPORTED");
                    break;
            }

            Console.WriteLine($" ==> Ship is here: ({shipX},{shipY}), facing direction {direction}");
        }

        private void MoveForward(int distance)
        {
            int realDirection = direction % 360;

            switch (realDirection)
            {
                case 0:
                case 360:
                case -360:
                    shipY += distance;
                    break;
                case 90:
                case -270:
                    shipX += distance;
                    break;
                case 180:
                case -180:
                    shipY -= distance;
                    break;
                case 270:
                case -90:
                    shipX -= distance;
                    break;


                default:
                    Console.WriteLine($"DIRECTION NOT SUPPORTED => {realDirection}");
                    break;
            }

        }

        internal int GetDistance()
        {
            //the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position
            return Math.Abs(shipX) + Math.Abs(shipY);
        }
    }
}