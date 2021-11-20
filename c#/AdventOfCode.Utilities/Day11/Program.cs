using AdventOfCode.Utilities;
using System;

namespace Day11
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("GetNumberOfOccupiedSeatsAtEnd?");

            long answer = GetNumberOfOccupiedSeatsAtEnd(ReadInput.GetChars("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetNumberOfOccupiedSeatsAtEnd(char[,] startingSeats)
        {
            long numberOfIterations = 0;
            char[,] finishingSeats = null;

            long numberOfOccupiedSeats = GetNumberOfOccupiedSeats(startingSeats);

            long numberOfSeatsChangedLastTime = GetNumberOfSeatsChanged(startingSeats, out finishingSeats);
            numberOfIterations++;
            numberOfOccupiedSeats = GetNumberOfOccupiedSeats(finishingSeats);
            Console.WriteLine($"After {numberOfIterations} iterations, numberOfSeatsChanged = {numberOfSeatsChangedLastTime}, numberOfOccupiedSeats = {numberOfOccupiedSeats}");

            startingSeats = finishingSeats;
            finishingSeats = null;

            while (true)
            {      
                long numberOfSeatsChanged = GetNumberOfSeatsChanged(startingSeats, out finishingSeats);
                numberOfIterations++;
                numberOfOccupiedSeats = GetNumberOfOccupiedSeats(finishingSeats);
                Console.WriteLine($"After {numberOfIterations} iterations, numberOfSeatsChanged = {numberOfSeatsChanged}, numberOfOccupiedSeats = {numberOfOccupiedSeats}");

                if (numberOfSeatsChanged == numberOfSeatsChangedLastTime)
                {
                    Print(finishingSeats);
                    return numberOfOccupiedSeats;
                }

                numberOfSeatsChangedLastTime = numberOfSeatsChanged;
                startingSeats = finishingSeats;
                finishingSeats = null;
            }
        }

        private static long GetNumberOfSeatsChanged(char[,] startingSeats, out char[,] finishingSeats)
        {
            int numberOfSeatsChanged = 0;

            int length = startingSeats.GetLength(0);
            int width = startingSeats.GetLength(1);
            finishingSeats = new char[length, width];

            for (int x = 0; x < length; x++)
            {
                for (int y = 0; y < width; y++)
                {
                    char seat = startingSeats[x, y];
                    finishingSeats[x, y] = seat;

                    if (seat == '.')
                    {
                        continue;
                    }

                    int occupiedSeats = GetNumberOfOccupiedSeatsAroundIgnoringFloor(startingSeats, length, width, x, y);

                    if (seat == 'L')
                    {
                        if (occupiedSeats == 0)
                        {
                            finishingSeats[x, y] = '#';
                            numberOfSeatsChanged++;
                            //Console.WriteLine($"Changed seat at [{x},{y}] from '{seat}' to '#'");
                        }
                    }
                    else if (seat == '#')
                    {
                        if (occupiedSeats >= 5)
                        {
                            finishingSeats[x, y] = 'L';
                            numberOfSeatsChanged++;
                            //Console.WriteLine($"Changed seat at [{x},{y}] from '{seat}' to 'L'");
                        }
                    }
                }
            }

            return numberOfSeatsChanged;
        } 

        private static int GetNumberOfOccupiedSeats(char[,] seats)
        {
            int occupiedSeats = 0;

            int length = seats.GetLength(0);
            int width = seats.GetLength(1);

            for (int x = 0; x < length; x++)
            {
                for (int y = 0; y < width; y++)
                {
                    char seat = seats[x, y];
                    //Console.Write(seat);
                    if (seat == '#')
                        occupiedSeats++;
                }
                //Console.WriteLine();
            }
            //Console.WriteLine($"occupiedSeats = {occupiedSeats}");
            //Console.WriteLine();

            return occupiedSeats;
        }



        private static void Print(char[,] seats)
        {
            int length = seats.GetLength(0);
            int width = seats.GetLength(1);

            for (int x = 0; x < length; x++)
            {
                for (int y = 0; y < width; y++)
                {
                    char seat = seats[x, y];
                    Console.Write(seat);
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        private static int GetNumberOfOccupiedSeatsAround(char[,] seats, int length, int width, int x, int y)
        {
            int occupiedSeats = 0;

            for (int xOffset = -1; xOffset <= 1; xOffset++)
            {
                int x2 = x + xOffset;

                if (x2 > -1 && x2 < length)
                {
                    for (int yOffset = -1; yOffset <= 1; yOffset++) //what do we do with floor?
                    {
                        int y2 = y + yOffset;

                        if (y2 > -1 && y2 < width)
                        {
                            if (!(x == x2 && y == y2))
                            {
                                if (seats[x2, y2] == '#')
                                    occupiedSeats++;
                            }
                        }
                    }
                }
            }

            return occupiedSeats;
        }

        private static int GetNumberOfOccupiedSeatsAroundIgnoringFloor(char[,] seats, int length, int width, int x, int y)
        {
            int occupiedSeats = 0;

            for (int xOffset = -1; xOffset <= 1; xOffset++)
            {
                for (int yOffset = -1; yOffset <= 1; yOffset++)
                {
                    if (!(xOffset == 0 && yOffset == 0))
                    {
                        bool isOccupied = IsNextSeatOccupied(seats, length, width, x, y, xOffset, yOffset);
                        if (isOccupied)
                            occupiedSeats++;
                    }                   
                }
            }

            return occupiedSeats;
        }

        private static bool IsNextSeatOccupied(char[,] seats, int length, int width, int x, int y, int xOffset, int yOffset)
        {
            int multiple = 1;

            while(true)
            {
                int x2 = x + xOffset * multiple;
                int y2 = y + yOffset * multiple;

                char? seat = TryToGetSeat(seats, length, width, x2, y2);

                if (seat == null)
                    return false;

                if (seats[x2, y2] == '#')
                    return true;

                if (seats[x2, y2] == 'L')
                    return false;
                
                multiple++;
            }
        }

        private static char? TryToGetSeat(char[,] seats, int length, int width, int x, int y)
        {
            if ((x > -1 && x < length) && (y > -1 && y < width))
                return seats[x, y];
            else 
                return null;
        }
    }
}
