using System;

namespace Day25
{
    class Program
    {
        static void Main(string[] args)
        {
            long pk1 = 19241437;
            long pk2 = 17346587;

            //long pk1 = 5764801;
            //long pk2 = 17807724;
                             
            //Then, a number of times called the loop size, perform the following steps:
            //Set the value to itself multiplied by the subject number.
            //Set the value to the remainder after dividing the value by 20201227.
           
            var loopSize1 = GetLoopSize(7, pk1);
            Console.WriteLine($"loopSize1: {loopSize1}");
            var loopSize2 = GetLoopSize(7, pk2);
            Console.WriteLine($"loopSize2: {loopSize2}");

            //The card transforms the subject number of the door's public key according to the card's loop size. The result is the encryption key.
            //The door transforms the subject number of the card's public key according to the door's loop size.The result is the same encryption key as the card calculated.
            var encryptionKey1 = Transform(pk1, loopSize2);
            Console.WriteLine($"encryptionKey1: {encryptionKey1}");

            var encryptionKey2 = Transform(pk2, loopSize1);
            Console.WriteLine($"encryptionKey2: {encryptionKey2}");
        }

        private static long GetLoopSize(long subjectNumber, long pk)
        {
            long value = 1;
            int i = 0;
            while (value != pk)
            {
                i++;
                value *= subjectNumber;
                value = value % 20201227;
                //Console.WriteLine($"{i}: {value}");
            }
            return i;
        }

        private static long Transform(long subjectNumber, long loopSize)
        {
            long value = 1;
            for (int i = 0; i < loopSize; i++)
            {
                value *= subjectNumber;
                value = value % 20201227;
                //Console.WriteLine($"{i}: {value}");
            }
            return value;
        }
    }
}
