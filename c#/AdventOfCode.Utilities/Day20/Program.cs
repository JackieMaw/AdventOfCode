using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;

namespace Day20
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What do you get if you multiply together the IDs of the four corner tiles?");

            var answer = GetCornerIDs(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetCornerIDs(string[] inputStrings)
        {
            var puzzlePieces = GetPuzzlePieces(inputStrings).ToArray();

            AddBorders(puzzlePieces);

            foreach (var p in puzzlePieces)
            {
                Console.WriteLine($"Puzzle {p.Id} has {p.Borders.Count} borders with {p.EdgeCount} edges { (p.EdgeCount == 2 ? "==> CORNER" : "")}");
            }

            var corners = puzzlePieces.Where(p => p.EdgeCount == 2).ToArray();

            var puzzle = AssemblePuzzle(puzzlePieces, corners[0]);

            var finalPuzzle = StripOffBorders(puzzle);

            DisplayPuzzle(finalPuzzle);

            (var numberOfSeaMonstersFound, var finalPuzzleWithMonsters) = FindSeaMonsters(finalPuzzle);

            Console.WriteLine($"numberOfSeaMonstersFound = {numberOfSeaMonstersFound}");

            DisplayPuzzle(finalPuzzleWithMonsters);

            return GetRoughness(finalPuzzleWithMonsters);

            //what's longer than a long????
            //A BigInteger!

            //return corners.Aggregate((BigInteger)1, (product, puzzle) => product * puzzle.Id);
        }

        private static long GetRoughness(char[,] puzzle)
        {
            int roughness = 0;
            int seaMonster = 0;

            for (int x = 0; x < puzzle.GetLength(0); x++)
            {
                for (int y = 0; y < puzzle.GetLength(1); y++)
                {
                    if (puzzle[x, y] == '#')
                        roughness++;

                    if (puzzle[x, y] == 'O')
                        seaMonster++;
                }
            }

            Console.WriteLine($"roughness = {roughness}");
            Console.WriteLine($"seaMonster = {seaMonster}");

            return roughness;
        }

        private static (long numberOfSeaMonstersFound, char[,] puzzle) FindSeaMonsters(char[,] puzzle)
        {
            List<(int x, int y)> seaMonster = GetSeaMonsterShape();

            for (int flipH = 0; flipH < 2; flipH++)
            {
                for (int flipV = 0; flipV < 2; flipV++)
                {
                    for (int rot = 0; rot < 4; rot++)
                    {
                        int numberOfSeaMonstersFound = CheckPuzzleForSeaMonsters(puzzle, seaMonster, flipH, flipV, rot);

                        if (numberOfSeaMonstersFound > 0)
                            return (numberOfSeaMonstersFound, puzzle);

                        puzzle = Rotate90(puzzle);
                    }
                    puzzle = FlipHorizontal(puzzle);
                }
                puzzle = FlipHorizontal(puzzle);
            }

            return (-1, null);
        }

        private static int CheckPuzzleForSeaMonsters(char[,] puzzle, List<(int x, int y)> seaMonster, int flipH, int flipV, int rot)
        {
            int numberOfSeaMonstersFound = 0;

            for (int x = 0; x < puzzle.GetLength(0) - 3; x++)
            {
                for (int y = 0; y < puzzle.GetLength(1) - 20; y++)
                {
                    bool found = CheckForSeaMonster(puzzle, seaMonster, x, y);
                    if (found)
                    {
                        Console.WriteLine($"SeaMonster found at ({x},{y}) on iteration {flipH} - {flipV} - {rot}");
                        numberOfSeaMonstersFound += 1;
                        DrawSeaMonster(puzzle, seaMonster, x, y);
                    }
                }
            }

            return numberOfSeaMonstersFound;
        }

        private static List<(int x, int y)> GetSeaMonsterShape()
        {
            var seaMonsterStrings = ReadInput.GetStrings("Seamonster.txt");

            List<(int x, int y)> seaMonster = new List<(int x, int y)>();
            for (int i = 0; i < seaMonsterStrings.Length; i++)
            {
                for (int j = 0; j < seaMonsterStrings[i].Length; j++)
                {
                    if (seaMonsterStrings[i][j] == '#')
                    {
                        seaMonster.Add((i, j));
                    }
                }
            }

            return seaMonster;
        }

        private static int GetRoughness(char[,] finalPuzzle, List<(int x, int y)> seaMonster, int i, int j)
        {
            int roughness = 0;
            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 20; y++)
                {
                    if (finalPuzzle[i + x, j + y] == '#')
                    {
                        if (!seaMonster.Contains((x, y)))
                        {
                            Console.Write(finalPuzzle[i + x, j + y]);
                            roughness++;
                        }
                        else 
                        {
                            Console.Write("O");
                        }
                    }
                    else
                        Console.Write(finalPuzzle[i + x, j + y]);
                }
                Console.WriteLine();
            }

            Console.WriteLine($"roughness: {roughness}");
            return roughness;
        }

        private static bool CheckForSeaMonster(char[,] finalPuzzle, List<(int x, int y)> seaMonster, int i, int j)
        {
            foreach (var sm in seaMonster)
            {
                if (finalPuzzle[i + sm.x, j + sm.y] != '#')
                    return false;
            }
            return true;
        }

        private static void DrawSeaMonster(char[,] finalPuzzle, List<(int x, int y)> seaMonster, int i, int j)
        {
            foreach (var sm in seaMonster)
            {
                finalPuzzle[i + sm.x, j + sm.y] = 'O';
            };
        }

        private static char[,] StripOffBorders(PuzzlePiece[,] puzzlePieces)
        {
            int numberOfPieces = puzzlePieces.GetLength(0);
            int pieceWidth = puzzlePieces[0, 0].Piece.GetLength(0);

            int puzzleSize = numberOfPieces * (pieceWidth - 2);
            char[,] puzzle = new char[puzzleSize, puzzleSize];

            for (int puzzleRow = 0; puzzleRow < numberOfPieces; puzzleRow++)
            {
                for (int puzzleCol = 0; puzzleCol < numberOfPieces; puzzleCol++)
                {
                    for (int row = 1; row < pieceWidth - 1; row++)
                    {
                        for (int col = 1; col < pieceWidth - 1; col++)
                        {
                            puzzle[puzzleRow * (pieceWidth - 2) + row - 1, puzzleCol * (pieceWidth - 2) + col - 1] = puzzlePieces[puzzleRow, puzzleCol].Piece[row, col];
                        }
                    }
                }
            }

            return puzzle;
        }

        private static void DisplayPuzzle(char[,] puzzle)
        {
            Console.WriteLine();
            for (int row = 0; row < puzzle.GetLength(0); row++)
            {
                for (int col = 0; col < puzzle.GetLength(1); col++)
                {
                    Console.Write(puzzle[row, col]);
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        private static PuzzlePiece[,] AssemblePuzzle(PuzzlePiece[] puzzlePieces, PuzzlePiece firstCorner)
        {
            var puzzleSize = (int)Math.Sqrt(puzzlePieces.Length);
            PuzzlePiece[,] puzzle = new PuzzlePiece[puzzleSize, puzzleSize];

            int pieceCounter = 1;

            Console.WriteLine($"ASSEMBLE PIECE #{pieceCounter} (0, 0)");
            //firstCorner.Display();
            RotateFirstCorner(firstCorner);
            //firstCorner.Display();

            puzzle[0, 0] = firstCorner;

            //do the first row
            for (int col = 1; col < puzzleSize; col++)
            {
                var previousPiece = puzzle[0, col - 1];
                var myBorder = previousPiece.RightBorder;

                var theirBorder = myBorder.Neighbour;
                PuzzlePiece nextPiece = theirBorder.Piece;

                pieceCounter++;
                Console.WriteLine($"ASSEMBLE PIECE #{pieceCounter} (0, {col})");

                //nextPiece.Display();
                RotateToLeftBorder(myBorder);
                //nextPiece.Display();

                puzzle[0, col] = nextPiece;
            }

            //do all the other rows
            for (int row = 1; row < puzzleSize; row++)
            {
                for (int col = 0; col < puzzleSize; col++)
                {
                    PuzzlePiece previousPiece = puzzle[row - 1, col];
                    PuzzleBorder myBorder = previousPiece.BottomBorder;

                    //DisplayPuzzle(puzzleSize, puzzle);
                    //Console.WriteLine("XXXX");
                    //Console.WriteLine();

                    pieceCounter++;
                    Console.WriteLine($"ASSEMBLE PIECE #{pieceCounter} ({row}, {col})");

                    PuzzleBorder theirBorder = myBorder.Neighbour;
                    PuzzlePiece nextPiece = theirBorder.Piece;

                    //nextPiece.Display();
                    RotateToTopBorder(myBorder);
                    //nextPiece.Display();

                    puzzle[row, col] = nextPiece;
                }
            }

            DisplayPuzzle(puzzleSize, puzzle);

            return puzzle;
        }

        private static void DisplayPuzzle(int puzzleSize, PuzzlePiece[,] puzzle)
        {
            for (int row = 0; row < puzzleSize; row++)
            {
                for (int col = 0; col < puzzleSize; col++)
                {
                    PuzzlePiece puzzlePiece = puzzle[row, col];
                    if (puzzlePiece == null)
                        return;
                    Console.Write(puzzlePiece.Id + " ");
                }
                Console.WriteLine();
            }
        }

        private static void RotateToTopBorder(PuzzleBorder myBorder)
        {
            var theirBorder = myBorder.Neighbour;

            //we want this neighbour's border to be at the TOP
            while (!IsTopBorder(theirBorder))
            {
                Console.WriteLine($"{theirBorder.Piece.Id} => Rotate90");
                theirBorder.Piece.Rotate90();
            }

            if (myBorder.Border != theirBorder.Border)
            {
                Console.WriteLine($"{theirBorder.Piece.Id} => FlipHorizontal");
                theirBorder.Piece.FlipHorizontal();
            }
        }

        private static bool IsTopBorder(PuzzleBorder border)
        {
            return border.BorderType == PuzzleBorder.Type.Top;
        }

        private static void RotateToLeftBorder(PuzzleBorder myBorder)
        {
            var theirBorder = myBorder.Neighbour;
            PuzzlePiece puzzlePieceToRotate = theirBorder.Piece;

            //we want this neighbour's border to be on the LEFT
            while (!IsLeftBorder(theirBorder))
            {
                Console.WriteLine($"{puzzlePieceToRotate.Id} => Rotate90");
                puzzlePieceToRotate.Rotate90();
            }

            if (myBorder.Border != theirBorder.Border)
            {
                Console.WriteLine($"{puzzlePieceToRotate.Id} => FlipVertical");
                puzzlePieceToRotate.FlipVertical();
            }

            if (theirBorder.Piece.TopBorder.Neighbour != null)
            {
                Console.WriteLine("Validation Failure - this piece should have no neighbour at the top!");
            }

            if (theirBorder.Piece.BottomBorder.Neighbour == null)
            {
                Console.WriteLine("Validation Failure - this piece should definately have a neighbour at the bottom!");
            }
        }
        private static bool IsLeftBorder(PuzzleBorder border)
        {
            return border.BorderType == PuzzleBorder.Type.Left;
        }

        private static void RotateFirstCorner(PuzzlePiece firstCorner)
        {
            //we want top and left borders to be null

            while (!IsTopLeftCorner(firstCorner))
            {
                Console.WriteLine($"{firstCorner.Id} => Rotate90");
                firstCorner.Rotate90();
            }
        }

        private static bool IsTopLeftCorner(PuzzlePiece piece)
        {
            return ((piece.TopBorder.Neighbour == null) && (piece.LeftBorder.Neighbour == null));
        }

        private static void AddBorders(IEnumerable<PuzzlePiece> puzzles)
        {
            Dictionary<string, PuzzleBorder> borders = new Dictionary<string, PuzzleBorder>();

            foreach (var puzzle in puzzles)
            {
                foreach (PuzzleBorder border in puzzle.Borders)
                {
                    if (borders.TryGetValue(border.Border, out PuzzleBorder neighbour))
                    {
                        border.Neighbour = neighbour;
                        neighbour.Neighbour = border;
                    }
                    else if (borders.TryGetValue(new string(border.Border.ToCharArray().Reverse().ToArray()), out PuzzleBorder neighbourReversed))
                    {
                        border.Neighbour = neighbourReversed;
                        neighbourReversed.Neighbour = border;
                    }
                    else
                    {
                        borders.Add(border.Border, border);
                    }
                }
            }
        }

        private static IEnumerable<PuzzlePiece> GetPuzzlePieces(string[] inputStrings)
        {
            List<string> puzzleStrings = new List<string>();
            foreach (var inputString in inputStrings)
            {
                if (string.IsNullOrEmpty(inputString))
                {
                    yield return new PuzzlePiece(puzzleStrings);
                    puzzleStrings = new List<string>();
                }
                else
                {
                    puzzleStrings.Add(inputString);
                }
            }
            yield return new PuzzlePiece(puzzleStrings);
        }

        public static char[,] Rotate90(char[,] puzzle)
        {
            int size = puzzle.GetLength(0);

            var newPuzzle = new char[size, size];

            for (int row = 0; row < size; row++)
            {
                for (int col = 0; col < size; col++)
                {
                    newPuzzle[col, size - row - 1] = puzzle[row, col];
                }
            }

            return newPuzzle;
        }

        public static char[,] FlipHorizontal(char[,] puzzle)
        {
            int size = puzzle.GetLength(0);

            var newPuzzle = new char[size, size];

            for (int row = 0; row < size; row++)
            {
                for (int col = 0; col < size; col++)
                {
                    newPuzzle[row, size - col - 1] = puzzle[row, col];
                }
            }

            return newPuzzle;
        }

        public static char[,] FlipVertical(char[,] puzzle)
        {
            int size = puzzle.GetLength(0);

            var newPuzzle = new char[size, size];

            for (int row = 0; row < size; row++)
            {
                for (int col = 0; col < size; col++)
                {
                    newPuzzle[size - row - 1, col] = puzzle[row, col];
                }
            }

            return newPuzzle;
        }
    }
}
