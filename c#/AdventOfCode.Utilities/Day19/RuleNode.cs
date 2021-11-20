using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Day19
{
    abstract internal class RuleNode
    {
        protected const int MAX_DEPTH = 100;
        public readonly string ruleNumber;
        public readonly string ruleLogic;

        private HashSet<string> validStrings = null;

        public HashSet<string> ValidStrings(int depth)
        {
            if (validStrings == null)
            {
                validStrings = GetValidStrings(depth);
            }
            return validStrings;
        }

        protected RuleNode(string ruleNumber, string ruleLogic)
        {
            this.ruleNumber = ruleNumber;
            this.ruleLogic = ruleLogic;
        }

        internal abstract void LinkToChildren(Dictionary<int, RuleNode> allRules);

        protected abstract HashSet<string> GetValidStrings(int depth);
        internal bool CheckAgainstAllValidStrings(string message)
        {
            if (ValidStrings(0).Contains(message))
                return true;

            return false;
        }

        abstract public bool IsValid(string message, int index);
        protected int ruleLength;
        public int RuleLength { get => ruleLength; }

        public override string ToString()
        {
            return ruleNumber + ": " + ruleLogic;
        }
    }

    internal class RuleNodeLeaf : RuleNode
    {
        char c;

        public RuleNodeLeaf(string ruleNumber, string ruleLogic):base(ruleNumber, ruleLogic)
        {
            //"b"
            c = ruleLogic[1];
            //ruleLength = 1;
        }

        internal override void LinkToChildren(Dictionary<int, RuleNode> allRules)
        { 
            //nothing to do here
        }

        public override bool IsValid(string message, int index)
        {
            return message[index] == c;
        }

        protected override HashSet<string> GetValidStrings(int depth)
        {
            var hashSet = new HashSet<string>();
            hashSet.Add($"{c}");
            return hashSet;
        }
    }

    internal abstract class RuleNodeBool : RuleNode
    {
        protected RuleNodeBool(string ruleNumber, string ruleLogic):base(ruleNumber, ruleLogic)
        {
        }

        public List<RuleNode> Children = new List<RuleNode>();
    }

    internal class RuleNodeOr : RuleNodeBool
    {
        public RuleNodeOr(string ruleNumber, string ruleLogic):base(ruleNumber, ruleLogic)
        {
        }

        internal override void LinkToChildren(Dictionary<int, RuleNode> allRules)
        {
            //1 3 | 3 1
            //always has exactly 2 AND children

            var ruleParts = ruleLogic.Split("|");

            int childNumber = 1;

            foreach (var rulePart in ruleParts)
            {
                var newChild = new RuleNodeAnd(ruleNumber + "." + childNumber, rulePart.Trim());
                newChild.LinkToChildren(allRules);
                Children.Add(newChild);

                childNumber++;
            }

            ruleLength = Children.Select(c => c.RuleLength).Max();
        }

        public override bool IsValid(string message, int index)
        {
            foreach (var child in Children)
            {
                if (child.IsValid(message, index))
                {
                    return true;
                }
            }
            return false;
        }

        protected override HashSet<string> GetValidStrings(int depth)
        {
            if (depth > MAX_DEPTH)
            {
                Console.WriteLine("MAX_DEPTH EXCEEDED");
                return new HashSet<string>();
            }

            var hashSet = new HashSet<string>();

            foreach (var chld in Children) //union hashsets
            {
                foreach (var s in chld.ValidStrings(depth + 1))
                {
                    hashSet.Add(s);
                }
            }

            return hashSet;
        }
    }

    internal class RuleNodeAnd : RuleNodeBool
    {

        public RuleNodeAnd(string ruleNumber, string ruleLogic):base(ruleNumber, ruleLogic)
        {
        }

        internal override void LinkToChildren(Dictionary<int, RuleNode> allRules)
        {
            //1 2 3
            //always links to pre-existing leaf nodes

            var ruleParts = ruleLogic.Split(" ");

            foreach (var rulePart in ruleParts)
            {
                int ruleNumber = Convert.ToInt32(rulePart);
                var child = allRules[ruleNumber];
                Children.Add(child);
            }

            ruleLength = Children.Select(c => c.RuleLength).Sum();
        }

        public override bool IsValid(string message, int index)
        {
            int i = index;
            foreach (var child in Children)
            {
                if (!child.IsValid(message, i))
                {
                    return false;
                }
                i += child.RuleLength; //might not be length 1!
            }
            return true;
        }

        protected override HashSet<string> GetValidStrings(int depth)
        {
            if (depth > MAX_DEPTH)
            {
                Console.WriteLine("MAX_DEPTH EXCEEDED");
                return new HashSet<string>();
            }

            List<string> validStrings = null;

            foreach (var chld in Children) //union hashsets
            {
                List<string> newValidStrings = new List<string>();
                if (validStrings == null)
                {
                    foreach (var s in chld.ValidStrings(depth + 1))
                    {
                        newValidStrings.Add(s);
                    }
                }
                else
                {
                    foreach (var vs in validStrings)
                    {
                        foreach (var s in chld.ValidStrings(depth + 1))
                        {
                            newValidStrings.Add(vs + s);
                        }
                    }
                }
                validStrings = newValidStrings;
            }

            return new HashSet<string>(validStrings);
        }
    }
}