using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day22
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("What is the winning player's score?");
            long answer = PlayTheGame(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long PlayTheGame(string[] inputStrings)
        {
            Queue<int> player1 = new Queue<int>();
            Queue<int> player2 = new Queue<int>();

            for (int i = 1; i < 26; i++)
            {
                player1.Enqueue(Convert.ToInt32(inputStrings[i]));
            }

            for (int i = 28; i < 53; i++)
            {
                player2.Enqueue(Convert.ToInt32(inputStrings[i]));
            }
                        
            var winner = Play(player1, player2);

            if (winner == "P1")
            {
                Console.WriteLine("Player 1 has won the game");
                return GetScore(player1);
            }
            else
            {
                Console.WriteLine("Player 2 has won the game");
                return GetScore(player2);
            }
        }

        private static string Play(Queue<int> player1, Queue<int> player2)
        {
            HashSet<string> previousRounds = new HashSet<string>();
            int round = 0;
            while (player1.Count > 0 && player2.Count > 0)
            {
                round++;
                var gameSnapshot = GetGameSnapshot(player1, player2);
                Console.WriteLine($"Round {round} - {gameSnapshot}");

                if (previousRounds.Contains(gameSnapshot))
                {
                    Console.WriteLine("Player 1 has won the game - infinite game prevention rule!");
                    return "P1";
                }
                else
                {
                    previousRounds.Add(gameSnapshot);
                }

                var card1 = player1.Dequeue();
                var card2 = player2.Dequeue();

                if (player1.Count >= card1 && player2.Count >= card2)
                {
                    //RECURSE
                    Console.WriteLine("WE CAN RECURSE");

                    var winner = Play(new Queue<int>(player1.Take(card1)), new Queue<int>(player2.Take(card2)));

                    if (winner == "P1")
                    {
                        Console.WriteLine("Player 1 has won the sub-game");
                        player1.Enqueue(card1);
                        player1.Enqueue(card2);
                    }
                    else
                    {
                        Console.WriteLine("Player 2 has won the sub-game");
                        player2.Enqueue(card2);
                        player2.Enqueue(card1);
                    }
                }
                else
                {
                    if (card1 > card2)
                    {
                        Console.WriteLine("Player 1 has won the round (cannot recurse)");
                        player1.Enqueue(card1);
                        player1.Enqueue(card2);
                    }
                    else if (card2 > card1)
                    {
                        Console.WriteLine("Player 2 has won the round (cannot recurse)");
                        player2.Enqueue(card2);
                        player2.Enqueue(card1);
                    }
                }
            }

            if (player1.Count > 0)
            {
                Console.WriteLine("Player 1 has won the game");
                return "P1";
            }
            else
            {
                Console.WriteLine("Player 2 has won the game");
                return "P2";
            }
        }

        private static string GetGameSnapshot(Queue<int> player1, Queue<int> player2)
        {
            return $"P1=({string.Join(",", player1)}) P2 = ({string.Join(",", player2)})";
        }

        private static int GetScore(Queue<int> player1)
        {
            var topCardValue = player1.Count;
            var score = 0;
            while (player1.Count > 0)
            {
                var card = player1.Dequeue();
                score += card * topCardValue;
                Console.WriteLine($"Score = {score} + {card} * {topCardValue}");
                topCardValue--;
            }

            return score;
        }
    }
}
