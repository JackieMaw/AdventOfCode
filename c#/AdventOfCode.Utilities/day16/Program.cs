using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;

namespace day16
{
    class Program
    {
        static void Main(string[] args)
        {
            //Console.WriteLine("Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?");

            //var answer = GetErrorScanningRate(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine("Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?");

            var answer = GetProductOfDepartureFields(ReadInput.GetStrings("Input.txt"), "departure");

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetProductOfDepartureFields(string[] inputs, string startswith)
        {
            var ticketScanner = ParseInputs(inputs);
            string[] fieldList = ticketScanner.GetValidFieldList();
            Console.WriteLine($"Final Field List: {string.Join(", ", fieldList)}");

            long product = 1;
            for (int i = 0; i < fieldList.Length; i++)
            {
                if (fieldList[i].StartsWith(startswith))
                {
                    product *= ticketScanner.MyTicket[i];
                    Console.WriteLine($"{fieldList[i]} => {ticketScanner.MyTicket[i]}");
                }
            }
            return product;
        }

        private static TicketScanner ParseInputs(string[] inputs)

        {
            int[] myTicket = null;
            List<int[]> otherTickets = new List<int[]>();
            List<string> ticketRules = new List<string>();
            bool myTicketSection = false;
            bool otherTicketSection = false;
            foreach (var input in inputs)
            {
                if (input == "nearby tickets:")
                {
                    otherTicketSection = true;
                }
                else if (input == "your ticket:")
                {
                    myTicketSection = true;
                }
                else if (otherTicketSection)
                {
                    if (input == "")
                    {
                        otherTicketSection = false;
                    }
                    else
                    {
                        otherTickets.Add(ReadInput.GetIntsFromSingleLine(input));
                    }
                }
                else if (myTicketSection)
                {
                    if (input == "")
                    {
                        myTicketSection = false;
                    }
                    else
                    {
                        myTicket = ReadInput.GetIntsFromSingleLine(input);
                    }
                }
                else
                {
                    if (input != "")
                    {
                        ticketRules.Add(input);
                    }
                }
            }

            return new TicketScanner(ticketRules, otherTickets, myTicket);
        }

        private static long GetErrorScanningRate(string[] inputs)        
        {
            var ticketScanner = ParseInputs(inputs);
            return ticketScanner.GetErrorScanningRate();
        }
    }
}
