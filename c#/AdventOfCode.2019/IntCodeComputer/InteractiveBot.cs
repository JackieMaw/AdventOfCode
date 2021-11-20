using System;
using System.Collections.Generic;
using System.Linq;

namespace MyComputer
{
    public class InteractiveBot : IDisposable, IBot
    {
        Queue<int> inputs = new Queue<int>();

        System.IO.StreamWriter streamWriter;
        public InteractiveBot()
        {
            streamWriter = System.IO.File.CreateText($"Input_Output_{DateTime.Now.ToString("yyyyMMdd_HHmm")}.txt");
        }
        private List<int> ToAscii(string myString)
        {
            return (myString + "\n").ToCharArray().Select(c => ((int)c)).ToList();
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
            ToAscii(inputString).ForEach(i => inputs.Enqueue(i));
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