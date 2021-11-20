using System;
using System.Collections.Generic;

namespace Day17
{
    internal class Space
    {
        HashSet<SpaceCube> activeSpaceCubes = new HashSet<SpaceCube>();

        SpaceCube min;
        SpaceCube max;

        public Space(char[,] initialSpace)
        {
            Initialize(initialSpace);

            min = new SpaceCube(0, 0, 0, 0);
            max = new SpaceCube(initialSpace.GetLength(0) - 1, initialSpace.GetLength(1) - 1, 0, 0);

            //PrintMe_Coordinates();
            //PrintMe();
        }

        private void Initialize(char[,] initialSpace)
        {
            for (int i = 0; i < initialSpace.GetLength(0); i++)
            {
                for (int j = 0; j < initialSpace.GetLength(1); j++)
                {
                    if (initialSpace[j, i] == '#')
                    {
                        activeSpaceCubes.Add(new SpaceCube(i, j, 0, 0));
                    }
                }
            }
        }

        private void PrintMe_Coordinates()
        {
            Console.WriteLine();

            for (int z = min.z; z <= max.z; z++)
            {
                Console.WriteLine($"z={z}");
                Console.WriteLine();

                for (int y = min.y; y <= max.y; y++)
                {
                    Console.Write($"{y,2} ");

                    for (int x = min.x; x <= max.x; x++)
                    {
                        Console.Write($"({x},{y},{z}) ");                        
                    }
                    Console.WriteLine();
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        private void PrintMe()
        {
            Console.WriteLine();

            for (int z = min.z; z <= max.z; z++)
            {
                Console.WriteLine($"z={z}");
                Console.WriteLine();

                Console.Write($"   ");
                for (int x = min.x; x <= max.x; x++)
                {
                    Console.Write($"{x,2}");
                }
                Console.WriteLine();

                for (int y = min.y; y <= max.y; y++)
                {
                    Console.Write($"{y,2} ");

                    for (int x = min.x; x <= max.x; x++)
                    {
                        var spaceCube = new SpaceCube(x, y, z, 0);
                        if (activeSpaceCubes.Contains(spaceCube))
                        {
                            Console.Write(" #");
                        }
                        else
                        {
                            Console.Write(" .");
                        }
                    }
                    Console.WriteLine();
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        internal void ChargeMe()
        {
            //If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.Otherwise, the cube becomes inactive.
            //If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

            var newActiveSpaceCubes = new HashSet<SpaceCube>();

            Console.WriteLine($"Checking Range from: ({min.x-1},{min.y-1},{min.z-1},{min.w-1}) to ({max.x+1},{max.y+1},{max.z+1},{max.w+1})...");

            for (int z = min.z - 1; z <= max.z + 1; z++) 
            {
                for (int x = min.x - 1; x <= max.x + 1; x++) 
                {
                    for (int y = min.y - 1; y <= max.y + 1; y++)
                    {
                        for (int w = min.w - 1; w <= max.w + 1; w++)
                        {
                            var spaceCube = new SpaceCube(x, y, z, w);
                            var neighbours = GetNumberOfActiveNeighbours(spaceCube);

                            if (activeSpaceCubes.Contains(spaceCube)) //this cube is active
                            {
                                if ((neighbours == 2) || (neighbours == 3)) //cube should remain active
                                {
                                    newActiveSpaceCubes.Add(spaceCube);
                                    //Console.WriteLine($"({x},{y},{z}) Active Cube will stay active");
                                }
                                else
                                {
                                    //Console.WriteLine($"({x},{y},{z}) Active Cube will become inactive");
                                }
                            }
                            else //cube is inactive
                            {
                                if (neighbours == 3)
                                {
                                    newActiveSpaceCubes.Add(spaceCube);
                                    //Console.WriteLine($"({x},{y},{z}) InActive Cube will become active");
                                }
                                else
                                {
                                    //Console.WriteLine($"({x},{y},{z}) InActive Cube will stay InActive");
                                }
                            }
                        }

                    }
                }
            }

            activeSpaceCubes = newActiveSpaceCubes;

            SetActiveRange();

            //PrintMe_Coordinates();
            //PrintMe();
        }

        private void SetActiveRange()
        {
            foreach (var spaceCube in activeSpaceCubes)
            {
                if (spaceCube.x < min.x)
                    min.x = spaceCube.x;

                if (spaceCube.x > max.x)
                    max.x = spaceCube.x;

                if (spaceCube.y < min.y)
                    min.y = spaceCube.y;

                if (spaceCube.y > max.y)
                    max.y = spaceCube.y;

                if (spaceCube.z < min.z)
                    min.z = spaceCube.z;

                if (spaceCube.z > max.z)
                    max.z = spaceCube.z;

                if (spaceCube.w < min.w)
                    min.w = spaceCube.w;

                if (spaceCube.w > max.w)
                    max.w = spaceCube.w;
            }
        }

        internal int GetNumberOfActiveNeighbours(SpaceCube spaceCube)
        {   
            int activeNeighbours = 0;

            for (int xOffset = -1; xOffset <= 1; xOffset++)
            {
                for (int yOffset = -1; yOffset <= 1; yOffset++)
                {
                    for (int zOffset = -1; zOffset <= 1; zOffset++)
                    {
                        for (int wOffset = -1; wOffset <= 1; wOffset++)
                        {
                            if (!(xOffset == 0 && yOffset == 0 && zOffset == 0 && wOffset == 0))
                            {
                                var neighbour = new SpaceCube(spaceCube.x + xOffset, spaceCube.y + yOffset, spaceCube.z + zOffset, spaceCube.w + wOffset);
                                if (activeSpaceCubes.Contains(neighbour))
                                    activeNeighbours++;
                            }
                        }
                    }
                }
            }

            return activeNeighbours;
        }

        internal long GetNumberOfActiveCubes()
        {
            return activeSpaceCubes.Count;
        }
    }
}