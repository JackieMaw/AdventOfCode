namespace Day18
{
    internal class Operand : MathNode
    {
        int value;

        public Operand(int value)
        {
            this.value = value;
        }

        internal override long Evaluate()
        {
            return value;
        }
        public override string ToString()
        {
            return $"{value}";
        }
    }
}