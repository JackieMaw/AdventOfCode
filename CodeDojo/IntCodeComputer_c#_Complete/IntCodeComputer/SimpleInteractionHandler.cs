using System;
using System.Collections.Generic;
using System.Linq;

namespace IntCodeComputer
{
    public class SimpleInteractionHandler : IDisposable, IInteractionHandler
    {
        Queue<long> inputQ;
        Queue<long> outputQ;
        System.IO.StreamWriter streamWriter;

        public SimpleInteractionHandler(Queue<long> inputQ, Queue<long> outputQ)
        {
            streamWriter = System.IO.File.CreateText($"InteractionLog_{DateTime.Now.ToString("yyyyMMdd_HHmm")}.txt");
            this.inputQ = inputQ;
            this.outputQ = outputQ;
        }

        public SimpleInteractionHandler():this(new Queue<long>(), new Queue<long>())
        {
        }

        private List<long> ToAscii(string myString)
        {
            return (myString + "\n").ToCharArray().Select(c => ((long)c)).ToList();
        }

        public long GetNextInput()
        {
            var input = inputQ.Dequeue();
            streamWriter.Write($"{(char)input}");
            streamWriter.Flush();
            return input;
        }

        public void Dispose()
        {
            streamWriter.Flush();
            streamWriter.Close();
        }

        public void SaveOutput(long output)
        {
            outputQ.Enqueue(output);
            streamWriter.Write($"{output}");
            streamWriter.Flush();
        }
    }
}