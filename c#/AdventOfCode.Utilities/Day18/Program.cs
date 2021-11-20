using AdventOfCode.Utilities;
using System;

namespace Day18
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Evaluate the expression on each line of the homework; what is the sum of the resulting values?");

            /*
            1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
            2 * 3 + (4 * 5) becomes 46.
            5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
            5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
            ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
            */

            long answer = new Calculator().DoMath("1 * 2 + 3");
            Console.WriteLine($"answer=5 ==> {answer}");

            answer = new Calculator().DoMath("1 + 2 * 3");
            Console.WriteLine($"answer=9 ==> {answer}");

            answer = new Calculator().DoMath("1 + (2 * 3) + (4 * (5 + 6))");
            Console.WriteLine($"answer=51 ==> {answer}");

            answer = new Calculator().DoMath("2 * 3 + (4 * 5)");
            Console.WriteLine($"answer=46 ==> {answer}");

            answer = new Calculator().DoMath("5 + (8 * 3 + 9 + 3 * 4 * 3)");
            Console.WriteLine($"answer=1445 ==> {answer}");

            answer = new Calculator().DoMath("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))");
            Console.WriteLine($"answer=669060 ==> {answer}");

            answer = new Calculator().DoMath("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2");
            Console.WriteLine($"answer=23340 ==> {answer}");

            /////////////////////////////////////////

            answer = 0;
            var maths = ReadInput.GetStrings("Input.txt");
            foreach (var m in maths)
            {
                answer += new Calculator().DoMath(m);
            }

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }
    }
}
