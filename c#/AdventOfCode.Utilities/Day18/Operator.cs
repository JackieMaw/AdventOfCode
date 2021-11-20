using System;

namespace Day18
{
    internal class Operator : MathNode
    {
        private string operation;
        private MathNode child1;
        private MathNode child2;

        public Operator(string operation, MathNode child1)
        {
            this.operation = operation;
            this.child1 = child1;

            if (child1 == null)
                throw new Exception("child1 cannot be null");
        }

        public void AddChild2(MathNode child2)
        {
            if (this.child2 != null)
                throw new Exception("child2 has already been set");

            this.child2 = child2;

            if (child2 == null)
                throw new Exception("child2 cannot be null");
        }

        internal override long Evaluate()
        {
            switch (operation)
            {
                case "+":
                    return child1.Evaluate() + child2.Evaluate();
                case "-":
                    return child1.Evaluate() - child2.Evaluate();
                case "*":
                    return child1.Evaluate() * child2.Evaluate();
                case "/":
                    return child1.Evaluate() / child2.Evaluate();
            }
            throw new Exception($"Operation Not Supported: {operation}");
        }

        public override string ToString()
        {
            return $"({child1} {operation} {child2})";
        }
    }
}