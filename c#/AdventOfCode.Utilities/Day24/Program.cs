using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;

namespace Day24
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("How many tiles are left with the black side up?");

            var answer = HowManyBlackTiles(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long HowManyBlackTiles(string[] instructions)
        {
            HashSet<(int x, int y)> blackTiles = new HashSet<(int x, int y)>();

            foreach (var instruction in instructions)
            {
                var xy = FollowInstruction(instruction);
                if (blackTiles.Contains(xy))
                {
                    blackTiles.Remove(xy);
                    Console.WriteLine($"({xy.x},{xy.y}) flipped back to WHITE");
                }
                else
                {
                    blackTiles.Add(xy);
                    Console.WriteLine($"({xy.x},{xy.y}) flipped to BLACK");
                }
            }

            Display(blackTiles);

            PlayTheGameOfLife(blackTiles);

            return blackTiles.Count;
        }

        private static void Display(HashSet<(int x, int y)> blackTiles)
        {
            (var min, var max) = GetMinMax(blackTiles);
            Console.WriteLine($"{min} => {max}");

            Console.WriteLine();
            for (int x = min.x - 2; x <= max.x + 2; x++)
            {
                //Console.WriteLine(x);
                for (int y = min.y - 2; y <= max.y + 2; y++)
                {
                    //either both even or both odd
                    if (((x % 2 == 0) && (y % 2 == 0)) || ((x % 2 != 0) && (y % 2 != 0)))
                    {
                        if (blackTiles.Contains((x, y)))
                            Console.Write("B");
                        else
                            Console.Write("W");
                    }
                    else
                    {
                        Console.Write("-");
                        continue;
                    }
                    //Console.Write(y);
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        private static void PlayTheGameOfLife(HashSet<(int, int)> blackTiles)
        {
            Console.WriteLine($"Day 0: {blackTiles.Count}");

            for (int i = 1; i <= 100; i++)
            {
                //Console.WriteLine($"SOD {i}: {blackTiles.Count}");

                (var min, var max) = GetMinMax(blackTiles);

                //Console.WriteLine($"{min} => {max}");

                var previousBlackTiles = new HashSet<(int, int)>(blackTiles);

                for (int x = min.x - 2; x <= max.x + 2; x++)
                {
                    for (int y = min.y - 2; y <= max.y + 2; y++)
                    {
                        //either both even or both odd
                        if (((x % 2 == 0) && (y % 2 == 0)) || ((x % 2 != 0) && (y % 2 != 0)))
                        {
                            //Console.WriteLine($"Checking ({x},{y})...");

                            var neighbours = GetNeighbours((x, y));

                            int countBlack = 0;
                            foreach (var n in neighbours)
                            {
                                if (previousBlackTiles.Contains(n))
                                    countBlack++;
                            }

                            bool isBlack = previousBlackTiles.Contains((x, y));

                            //Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
                            if (isBlack)
                            {
                                if ((countBlack == 0) || (countBlack > 2))
                                {
                                    blackTiles.Remove((x, y));
                                    //Console.WriteLine($"({x},{y}) flipped back to WHITE");
                                }
                            }
                            //Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
                            else
                            {
                                if (countBlack == 2)
                                {
                                    blackTiles.Add((x, y));
                                    //Console.WriteLine($"({x},{y}) flipped to BLACK");
                                }

                            }
                        }
                    }
                }

                Console.WriteLine($"EOD {i}: {blackTiles.Count}");
            }
        }

        private static ((int x, int y) min, (int x, int y) max) GetMinMax(HashSet<(int x, int y)> blackTiles)
        {
            (int x, int y) min = (int.MaxValue, int.MaxValue);
            (int x, int y) max = (0, 0);

            foreach (var xy in blackTiles)
            {
                if (xy.x < min.x)
                    min.x = xy.x;

                if (xy.y < min.y)
                    min.y = xy.y;

                if (xy.x > max.x)
                    max.x = xy.x;

                if (xy.y > max.y)
                    max.y = xy.y;
            }

            return (min, max);
        }

        private static List<(int x, int y)> GetNeighbours((int x, int y) xy)
        {
            return new List<(int x, int y)>
            {
                (xy.x + 2, xy.y),   //e
                (xy.x - 2, xy.y),  //w
                (xy.x + 1, xy.y - 1),      //se
                (xy.x - 1, xy.y - 1), //sw
                (xy.x + 1, xy.y + 1), //ne
                (xy.x - 1, xy.y + 1), //nw
            };
        }

        private static (int x, int y) FollowInstruction(string instruction)
        {
            (var x, var y) = (0, 0);

            //e, se, sw, w, nw, and ne

            int index = 0;

            while (index < instruction.Length)
            {
                switch (instruction[index])
                {
                    case 'e':
                        x += 2;
                        break;
                    case 'w':
                        x -= 2;
                        break;
                    case 's':
                        index++;
                        switch (instruction[index])
                        {
                            case 'e':
                                x += 1;
                                y -= 1;
                                break;
                            case 'w':
                                x -= 1;
                                y -= 1;
                                break;
                            default:
                                break;
                        }
                        break;
                    case 'n':
                        index++;
                        switch (instruction[index])
                        {
                            case 'e':
                                x += 1;
                                y += 1;
                                break;
                            case 'w':
                                x -= 1;
                                y += 1;
                                break;
                            default:
                                break;
                        }
                        break;
                    default:
                        break;
                }

                index++;
            }

            return (x, y);
        }
    }
}
