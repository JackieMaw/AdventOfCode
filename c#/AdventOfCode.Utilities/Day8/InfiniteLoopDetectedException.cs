using System;
using System.Runtime.Serialization;

namespace Day8
{
    [Serializable]
    internal class InfiniteLoopDetectedException : Exception
    {
        public InfiniteLoopDetectedException()
        {
        }

        public InfiniteLoopDetectedException(string message) : base(message)
        {
        }

        public InfiniteLoopDetectedException(string message, Exception innerException) : base(message, innerException)
        {
        }

        protected InfiniteLoopDetectedException(SerializationInfo info, StreamingContext context) : base(info, context)
        {
        }
    }
}