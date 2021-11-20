using System;
using System.Collections.Generic;
using System.Linq;

namespace MyComputer
{
    public class StupidBot : IDisposable, IBot
    {
        List<int> inputs = new List<int>();
        int inputCounter = 0;

        System.IO.StreamWriter streamWriter;
        public StupidBot()
        {
            inputs.AddRange(ToAscii("A,B,A,B,A,C,B,C,A,C"));
            inputs.AddRange(ToAscii("L,6,R,12,L,6"));
            inputs.AddRange(ToAscii("R,12,L,10,L,4,L,6"));
            inputs.AddRange(ToAscii("L,10,L,10,L,4,L,6"));
            inputs.AddRange(ToAscii("n"));

            streamWriter = System.IO.File.CreateText("Input_Output.txt");
        }
        private int[] ToAscii(string myString)
        {
            return (myString + "\n").ToCharArray().Select(c => ((int)c)).ToArray();
        }

        public long GetNextInput()
        {
            var input = inputs[inputCounter++];
            streamWriter.Write($"{(char)input}");
            Console.Write($"{(char)input}");
            return input;
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
        }
    }
}