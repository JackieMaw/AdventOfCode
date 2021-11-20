using System.Collections.Generic;

namespace Day19
{
    public static class StackExtensions
    {
        public static Stack<T> Clone<T>(this Stack<T> stack)
        {
            return new Stack<T>(new Stack<T>(stack));
        }
    }
}