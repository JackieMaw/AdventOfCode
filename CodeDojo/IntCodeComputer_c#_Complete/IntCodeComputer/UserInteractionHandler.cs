using System;
using System.Collections.Generic;
using System.Linq;

namespace IntCodeComputer
{
    public class UserInteractionHandler : IDisposable, IInteractionHandler
    {
        Queue<long> inputs = new Queue<long>();

        System.IO.StreamWriter streamWriter;
        public UserInteractionHandler()
        {
            streamWriter = System.IO.File.CreateText($"InteractionLog_{DateTime.Now.ToString("yyyyMMdd_HHmm")}.txt");
        }

        private List<long> ConvertFromTextToAsciiCode(string myString)
        {
            return (myString + "\n").ToCharArray().Select(c => ((long)c)).ToList();
        }

        public long GetNextInput()
        {
            if (!inputs.Any())
            {
                //no recorded input left, ask the user
                GetInputFromUser();
            }

            var input = inputs.Dequeue();
            streamWriter.Write($"{(char)input}");
            //Console.Write($"{(char)input}");
            streamWriter.Flush();

            return input;
        }

        private void GetInputFromUser()
        {
            streamWriter.Write(">>");
            Console.WriteLine(">>");
            var inputString = Console.ReadLine();
            if (inputString != null)
                ConvertFromTextToAsciiCode(inputString).ForEach(i => inputs.Enqueue(i));
        }

        public void Dispose()
        {
            streamWriter.Flush();
            streamWriter.Close();
        }

        public void SaveOutput(long output)
        {
            if (output < 128)
            {
                Console.Write($"{(char)output}");
                streamWriter.Write($"{(char)output}");
            }
            else
            {
                Console.Write($"{output}");
                streamWriter.Write($"{output}");
            }
            streamWriter.Flush();
        }
    }
}