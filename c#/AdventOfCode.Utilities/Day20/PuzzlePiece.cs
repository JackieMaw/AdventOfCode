using System;
using System.Collections.Generic;
using System.Linq;

namespace Day20
{
    internal class PuzzlePiece
    {
        public readonly int Id;

        public readonly List<PuzzleBorder> Borders;
        public int EdgeCount => Borders.Where(b => b.Neighbour == null).Count();

        public char[,] Piece;

        public PuzzlePiece(List<string> puzzleStrings)
        {
            //Tile 2971:
            //..#.#....#
            Id = Convert.ToInt32(puzzleStrings[0].Substring(5, 4));

            Borders = new List<PuzzleBorder>();

            int pieceSize = puzzleStrings.Count() - 1;
            Piece = new char[pieceSize, pieceSize];

            var leftBorder = "";
            var rightBorder = "";
            for (int row = 0; row < pieceSize; row++)
            {
                string puzzleString = puzzleStrings[row + 1];

                if (row == 0)
                {
                    Borders.Add(new PuzzleBorder(puzzleString, this, PuzzleBorder.Type.Top));
                }

                leftBorder += puzzleString[0];
                rightBorder += puzzleString[pieceSize - 1];

                if (row == pieceSize - 1)
                {
                    Borders.Add(new PuzzleBorder(puzzleString, this, PuzzleBorder.Type.Bottom));
                }

                for (int col = 0; col < pieceSize; col++)
                {
                    Piece[row, col] = puzzleString[col];
                }
            }

            Borders.Add(new PuzzleBorder(leftBorder, this, PuzzleBorder.Type.Left));
            Borders.Add(new PuzzleBorder(rightBorder, this, PuzzleBorder.Type.Right));
        }

        internal PuzzleBorder GetBorder(PuzzleBorder.Type borderType)
        {
            return Borders.Where(b => b.BorderType == borderType).First();
        }

        public PuzzleBorder TopBorder => GetBorder(PuzzleBorder.Type.Top);
        public PuzzleBorder BottomBorder => GetBorder(PuzzleBorder.Type.Bottom);
        public PuzzleBorder RightBorder => GetBorder(PuzzleBorder.Type.Right);
        public PuzzleBorder LeftBorder => GetBorder(PuzzleBorder.Type.Left);

        internal void Rotate90()
        {
            int pieceSize = Piece.GetLength(0);

            var newPuzzle = new char[pieceSize, pieceSize];

            for (int row = 0; row < pieceSize; row++)
            {
                for (int col = 0; col < pieceSize; col++)
                {
                    newPuzzle[col, pieceSize - row - 1] = Piece[row, col];
                }
            }

            Piece = newPuzzle;

            var topBorder = TopBorder;
            var rightBorder = RightBorder;
            var bottomBorder = BottomBorder;
            var leftBorder = LeftBorder;

            topBorder.BorderType = PuzzleBorder.Type.Right;
            rightBorder.BorderType = PuzzleBorder.Type.Bottom;
            bottomBorder.BorderType = PuzzleBorder.Type.Left;
            leftBorder.BorderType = PuzzleBorder.Type.Top;

            ResetBorders();
        }

        private void ResetBorders()
        {
            int pieceSize = GetPieceSize();

            var leftBorder = "";
            var rightBorder = "";
            for (int row = 0; row < pieceSize; row++)
            {
                if (row == 0)
                {
                    var topBorder = "";
                    for (int col = 0; col < pieceSize; col++)
                    {
                        topBorder += Piece[row, col];
                    }
                    TopBorder.Border = topBorder;
                }
                else if (row == GetPieceSize() - 1)
                {
                    var bottomBorder = "";
                    for (int col = 0; col < pieceSize; col++)
                    {
                        bottomBorder += Piece[row, col];
                    }
                    BottomBorder.Border = bottomBorder;
                }

                leftBorder += Piece[row, 0];
                rightBorder += Piece[row, pieceSize - 1];
            }

            LeftBorder.Border = leftBorder;
            RightBorder.Border = rightBorder;

        }

        internal void Display()
        {
            Console.WriteLine();
            Console.WriteLine($"Id: {Id}");
            TopBorder.Display();
            RightBorder.Display();
            BottomBorder.Display();
            LeftBorder.Display();
            Console.WriteLine();

            int pieceSize = GetPieceSize();
            for (int row = 0; row < pieceSize; row++)
            {
                for (int col = 0; col < pieceSize; col++)
                {
                    Console.Write(Piece[row, col]);
                }
                Console.WriteLine();
            }
            Console.WriteLine();
        }

        private int GetPieceSize()
        {
            return Piece.GetLength(0);
        }

        public void FlipVertical()
        {
            int pieceSize = Piece.GetLength(0);

            var newPuzzle = new char[pieceSize, pieceSize];

            //column stays the same, row flips
            for (int row = 0; row < pieceSize; row++)
            {
                for (int col = 0; col < pieceSize; col++)
                {
                    newPuzzle[pieceSize - row - 1, col] = Piece[row, col];
                }
            }

            Piece = newPuzzle;

            //top and bottom borders swap
            var topBorder = TopBorder;
            var bottomBorder = BottomBorder;
            topBorder.BorderType = PuzzleBorder.Type.Bottom;
            bottomBorder.BorderType = PuzzleBorder.Type.Top;

            ResetBorders();
        }

        internal void FlipHorizontal()
        {
            int pieceSize = Piece.GetLength(0);

            var newPuzzle = new char[pieceSize, pieceSize];

            //row stays the same, column flips
            for (int row = 0; row < pieceSize; row++)
            {
                for (int col = 0; col < pieceSize; col++)
                {
                    newPuzzle[row, pieceSize - col - 1] = Piece[row, col];
                }
            }

            Piece = newPuzzle;

            //left and right borders swap
            var rightBorder = RightBorder;
            var leftBorder = LeftBorder;
            rightBorder.BorderType = PuzzleBorder.Type.Left;
            leftBorder.BorderType = PuzzleBorder.Type.Right;

            ResetBorders();
        }

        public override string ToString()
        {
            return $"{Id}: {TopBorder.ToString() ?? "null"}, {RightBorder.ToString() ?? "null"}, {BottomBorder.ToString() ?? "null"}, {LeftBorder.ToString() ?? "null"}";
        }
    }
}