using System;
using System.Collections.Generic;
using System.Linq;

namespace day16
{
    internal class TicketScanner
    {
        private readonly TicketRule[] TicketRules;
        public readonly int[] MyTicket;
        private readonly List<int[]> OtherTickets;

        public TicketScanner(List<string> ticketRuleStrings, List<int[]> otherTickets, int[] myTicket)
        {
            TicketRules = ticketRuleStrings.Select(s => new TicketRule(s)).ToArray();
            OtherTickets = otherTickets;
            MyTicket = myTicket;
        }

        internal long GetErrorScanningRate()
        {
            HashSet<int> validValues = GetValidValues();

            int sumOfInvalidValues = 0;
            foreach (var otherTickets in OtherTickets)
            {
                foreach (var ticketField in otherTickets)
                {
                    if (!validValues.Contains(ticketField))
                    {
                        Console.WriteLine($"Invalid Value: {ticketField}");
                        sumOfInvalidValues += ticketField;
                    }
                }
            }

            return sumOfInvalidValues;
        }

        private HashSet<int> GetValidValues()
        {
            HashSet<int> validValues = new HashSet<int>();
            foreach (var ticketRule in TicketRules)
            {
                foreach (var validInt in ticketRule.ValidRange)
                {
                    validValues.Add(validInt);
                }
            }

            return validValues;
        }

        internal string[] GetValidFieldList()
        {
            HashSet<int> validValues = GetValidValues();

            List<int[]> otherValidTickets = new List<int[]>();
            foreach (var otherTicket in OtherTickets)
            {
                bool isValid = true;
                foreach (var ticketField in otherTicket)
                {
                    if (!validValues.Contains(ticketField))
                    {
                        Console.WriteLine($"Invalid Value: {ticketField}");
                        isValid = false;
                    }
                }

                if (isValid)
                {
                    otherValidTickets.Add(otherTicket);
                }
            }

            List<List<TicketRule>> possibleFieldsForEachField = new List<List<TicketRule>>();

            for (int i = 0; i < TicketRules.Count(); i++)
            {
                possibleFieldsForEachField.Add(new List<TicketRule>(TicketRules));
            }

            foreach (var otherValidTicket in otherValidTickets)
            {
                for (int i = 0; i < otherValidTicket.Length; i++)
                {
                    var thisFieldValue = otherValidTicket[i];
                    var listOfPossibleFields = possibleFieldsForEachField[i];

                    var listOfImpossibleFields = new List<TicketRule>();

                    foreach (var possibleField in listOfPossibleFields)
                    {
                        if (!possibleField.ValidRange.Contains(thisFieldValue))
                        {
                            listOfImpossibleFields.Add(possibleField);
                        }
                    }

                    foreach (var impossibleField in listOfImpossibleFields)
                    {
                        listOfPossibleFields.Remove(impossibleField);
                        Console.WriteLine($"Must exclude {impossibleField.Fieldname} for Field #{i}");
                    }
                }
            }

            //must apply process of elimination

            List<int> fieldsToFinalize = new List<int>();
            HashSet<string> fieldsFinalised = new HashSet<string>();
            string[] fields = new string[possibleFieldsForEachField.Count()];
            for (int i = 0; i < possibleFieldsForEachField.Count; i++)
            {
                var listOfPossibleFields = possibleFieldsForEachField[i];
                if (listOfPossibleFields.Count() == 1)
                {
                    fieldsFinalised.Add(listOfPossibleFields[0].Fieldname);
                    fields[i] = listOfPossibleFields[0].Fieldname;
                }
                else
                {
                    fieldsToFinalize.Add(i);
                }
            }

            while(fieldsToFinalize.Count() > 0)
            {
                Console.WriteLine($"fieldsToFinalize.Count(): {fieldsToFinalize.Count()}");

                List<int> fieldsJustFinalized = new List<int>();
                foreach (var i in fieldsToFinalize)
                {
                    var listOfPossibleFields = possibleFieldsForEachField[i];

                    var listOfImpossibleFields = new List<TicketRule>();
                    foreach (var possibleField in listOfPossibleFields)
                    {
                        if (fieldsFinalised.Contains(possibleField.Fieldname))
                            listOfImpossibleFields.Add(possibleField);
                    }

                    foreach (var impossibleField in listOfImpossibleFields)
                    {
                        listOfPossibleFields.Remove(impossibleField);
                        Console.WriteLine($"Must exclude {impossibleField.Fieldname} for Field #{i}");
                    }

                    if (listOfPossibleFields.Count() == 1)
                    {
                        fieldsFinalised.Add(listOfPossibleFields[0].Fieldname);
                        fields[i] = listOfPossibleFields[0].Fieldname;
                        fieldsJustFinalized.Add(i);
                    }
                }

                foreach (var i in fieldsJustFinalized)
                {
                    fieldsToFinalize.Remove(i);
                }
            }

            foreach (var possibleFields in possibleFieldsForEachField)
            {
                if (possibleFields.Count() > 1)
                {
                    Console.WriteLine("ERROR!!!!");
                }
            }

            return fields;
        }
    }
}