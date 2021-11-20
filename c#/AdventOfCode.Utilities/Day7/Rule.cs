using System;
using System.Collections.Generic;
using System.Linq;

namespace Day7
{
    //this is a directed graph, we assume no loops!
    internal class Rule
    {
        private string myBagColour;
        private string ruleString;
        private long? sum = null;

        private List<Tuple<int, Rule>> childRules; //null to indicate not initialized yet

        public string Key { get { return myBagColour; } }

        public Rule(string ruleString)
        {
            //shiny gray bags contain 4 dark teal bags, 1 wavy crimson bag, 4 posh lime bags.
            this.ruleString = ruleString;
            this.myBagColour = GetColour(ruleString);
        }

        private string GetColour(string ruleString) //text manipulation
        {
            //shiny gray
            return CleanString(ruleString.Split("contain")[0].Replace("bags", ""));
        }

        public void AddChildRules(Dictionary<string, Rule> allRules) //text manipulation
        {
            childRules = new List<Tuple<int, Rule>>();

            //4 dark teal bags, 1 wavy crimson bag, 4 posh lime bags.
            var childRuleStrings = ruleString.Split("contain")[1].Split(",").Select(s => CleanString(s));

            foreach (var childRuleString in childRuleStrings)
            {
                //4 dark teal
                //1 wavy crimson
                //4 posh lime
                //no other

                if (childRuleString != "no other") //base case
                {
                    var indexOfFirstSpace = childRuleString.IndexOf(" ");

                    int numberOfBags = Convert.ToInt32(childRuleString.Substring(0, indexOfFirstSpace));

                    string childBagColour = childRuleString.Substring(indexOfFirstSpace + 1);

                    var childRule = allRules[childBagColour];

                    childRules.Add(new Tuple<int, Rule>(numberOfBags, childRule));
                }
            }
        }

        public string CleanString(string s)
        {
            return s.Replace("bags", "").Replace("bag", "").Replace(".", "").Trim();
        }

        internal long GetNumberOfBagsWhichCanContain(string bagColour) //recursive graph traversal
        {
            if (sum.HasValue) //already calculated this sub-tree
                return sum.Value;

            sum = 0;

            if (bagColour != myBagColour) //base case - STOP RECURSION
            {
                foreach (var childRuleTuple in childRules) //sum up the children
                {
                    var numberOfBags = childRuleTuple.Item1;
                    var childRule = childRuleTuple.Item2;
                    if (childRule.Key == bagColour)
                    {
                        sum += 1;
                    }
                    else
                    {
                        sum += childRule.GetNumberOfBagsWhichCanContain(bagColour) * numberOfBags;
                    }
                }
            }

            Console.WriteLine($"{myBagColour} can contain {sum} x {bagColour}");
            return sum.Value;
        }

        internal long GetNumberOfBags() //recursive graph traversal
        {
            if (sum.HasValue) //already calculated this sub-tree
                return sum.Value;

            sum = 1; //include me = BASE CASE

            foreach (var childRuleTuple in childRules) //sum up the children
            {
                var numberOfBags = childRuleTuple.Item1;
                var childRule = childRuleTuple.Item2;
                sum += childRule.GetNumberOfBags() * numberOfBags;
            }

            Console.WriteLine($"{myBagColour} must contain exactly {sum} x bags");
            return sum.Value;
        }
    }
}