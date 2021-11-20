using AdventOfCode.Utilities;
using System;
using System.Linq;
using System.Collections.Generic;

namespace Day19
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("How many messages completely match rule 0?");

            long answer = HowManyMessagesMatchRule0(ReadInput.GetStrings("Input_WithLoops.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long HowManyMessagesMatchRule0(string[] inputStrings)
        {
            var rules = inputStrings.TakeWhile(s => !string.IsNullOrEmpty(s)).ToArray();

            Dictionary<int, RuleNode> allRules = GetAllRules(rules);

            var messages = inputStrings.TakeLast(inputStrings.Length - rules.Length - 1).ToArray();

            //Console.WriteLine();
            //Console.WriteLine("RULE 8");
            //Console.WriteLine();
            //foreach (var validString in allRules[8].ValidStrings(0))
            //{
            //    Console.WriteLine($"   {validString}");
            //}

            //Console.WriteLine();
            //Console.WriteLine("RULE 11");
            //Console.WriteLine();
            //foreach (var validString in allRules[11].ValidStrings(0))
            //{
            //    Console.WriteLine($"   {validString}");
            //}

            //Console.WriteLine();
            //Console.WriteLine("RULE 31");
            //Console.WriteLine();
            //foreach (var validString in allRules[31].ValidStrings(0))
            //{
            //    Console.WriteLine($"   {validString}");
            //}

            //Console.WriteLine();
            //Console.WriteLine("RULE 42");
            //Console.WriteLine();
            //foreach (var validString in allRules[42].ValidStrings(0))
            //{
            //    Console.WriteLine($"   {validString}");
            //}

            var rule0 = allRules[0];
            //var validStrings = rule0.ValidStrings(0);
            //Console.WriteLine();
            //foreach (var validString in validStrings)
            //{
            //    Console.WriteLine($"   {validString}");
            //}

            //Console.WriteLine();
            //Console.WriteLine($"{validStrings.Count} Valid Strings");
            //Console.WriteLine();

            int validMessages = 0;
            foreach (var message in messages)
            {
                if (Match(message, rule0))
                //if (rule0.CheckAgainstAllValidStrings(message))
                    //if (rule0.IsValid(message, 0))
                    validMessages++;
            }

            return validMessages;
        }

        private static bool Match(string message, RuleNode rule)
        {
            Stack<RuleNode> stack = new Stack<RuleNode>();
            stack.Push(rule);
            return Match(message, 0, stack);

        }

        private static bool Match(string message, int index, Stack<RuleNode> stack)
        {
            while (stack.Any() && index < message.Length)
            {
                //Console.WriteLine("Message: " + message.Substring(index));
                //Console.WriteLine("Stack: " + string.Join(", ", stack.Select(s => s.ruleNumber)));
                var rule = stack.Pop();
                //Console.WriteLine("Popped: " + rule);

                if (rule is RuleNodeLeaf)
                {
                    if (rule.IsValid(message, index))
                    {
                        return Match(message, index + 1, stack.Clone());
                    }
                    else
                    {
                        return false;
                    }
                }
                else if (rule is RuleNodeAnd)
                {
                    var childRules = new List<RuleNode>(((RuleNodeAnd)rule).Children);
                    childRules.Reverse();
                    foreach (var childRule in childRules) //replace with all the child rules
                    {
                        stack.Push(childRule);
                    }
                }
                else if (rule is RuleNodeOr)
                {
                    var childRules = new List<RuleNode>(((RuleNodeOr)rule).Children);
                    foreach (var childRule in childRules)
                    {
                        stack.Push(childRule);

                        if (Match(message, index, stack.Clone()))
                        {
                            return true;
                        }

                        stack.Pop(); //abandon this child rule
                    }
                    //none of the child rules matches
                    return false;
                }
            }

            if (!stack.Any() && (index == message.Length))
                return true;
            else
                return false;
        }

        private static Dictionary<int, RuleNode> GetAllRules(string[] rules)
        {
            /*
            0: 1 2
            1: "a"
            2: 1 3 | 3 1
            3: "b"
             */

            Dictionary<int, RuleNode> allRules = new Dictionary<int, RuleNode>();

            foreach (var ruleString in rules)
            {
                var ruleParts = ruleString.Split(":");
                var ruleNumber = Convert.ToInt32(ruleParts[0]);
                var ruleLogic = ruleParts[1].Trim();

                if (ruleString.Contains('"'))
                    allRules.Add(ruleNumber, new RuleNodeLeaf(ruleParts[0], ruleLogic));
                else if (ruleString.Contains('|'))
                    allRules.Add(ruleNumber, new RuleNodeOr(ruleParts[0], ruleLogic));
                else //And
                    allRules.Add(ruleNumber, new RuleNodeAnd(ruleParts[0], ruleLogic));
            }

            foreach (var pair in allRules)
            {
                pair.Value.LinkToChildren(allRules);
            }

            return allRules;
        }
    }
}
