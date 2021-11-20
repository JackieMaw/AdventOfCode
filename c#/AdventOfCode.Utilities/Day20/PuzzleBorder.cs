using System;
using System.Collections.Generic;

namespace Day20
{
    internal class PuzzleBorder
    {
        public enum Type
        {
            Top, Bottom, Left, Right
        }

        public string Border;
        public readonly PuzzlePiece Piece;
        public Type BorderType;

        public PuzzleBorder Neighbour;

        public PuzzleBorder(string border, PuzzlePiece puzzle, Type borderType)
        {
            Border = border;
            Piece = puzzle;
            BorderType = borderType;
        }
        public override string ToString()
        {
            return $"{BorderType}=>{Neighbour?.Piece.Id.ToString()}";
        }

        internal void Display()
        {
            if (Neighbour != null)
                Console.WriteLine($"My {BorderType} => {Neighbour.Piece.Id} [{Border}] which is Her {Neighbour.BorderType} [{Neighbour.Border}]");
        }
    }
}