using System;
using System.Collections.Generic;

namespace MyComputer
{
    internal class ItemJuggler
    {
        private readonly Queue<Queue<string>> allAttempts;
        private Queue<string> currentAttempt;

        private int attemptCount = 0;

        public ItemJuggler(string[] items)
        {
            this.allAttempts = GetAllAttempts(items);
        }

        private Queue<Queue<string>> GetAllAttempts(string[] items)
        {
            Queue<Queue<string>> allAttempts = new Queue<Queue<string>>();

            var itemCount = items.Length;

            for (int i = 0; i < Math.Pow(2, itemCount); i++)
            {
                var binaryString = Convert.ToString(i, 2);

                Queue<string> currentAttempt = new Queue<string>();

                for (int j = 0; j < itemCount; j++)
                {
                    bool takeItem;
                    if (j < binaryString.Length)
                    {
                        takeItem = binaryString[binaryString.Length - j - 1] == '1';
                    }
                    else
                    {
                        takeItem = false;
                    }

                    var action = takeItem ? "take" : "drop";
                    currentAttempt.Enqueue($"{action} {items[j]}");
                }

                currentAttempt.Enqueue("inv");
                currentAttempt.Enqueue("west");
                allAttempts.Enqueue(currentAttempt);
            }

            return allAttempts;
        }

        internal string GetNextInstruction()
        {
            try
            {
                if (currentAttempt == null || currentAttempt.Count == 0)
                {
                    currentAttempt = allAttempts.Dequeue();
                    Console.WriteLine($"Beginning attempt #{attemptCount++}...");
                }

                return currentAttempt.Dequeue();
            }
            catch (Exception)
            {
                return null;
            }
        }
    }
}