using System;
using System.Collections.Generic;
using System.Linq;

namespace Day18
{
    internal class Calculator
    {
        int mathPointer = 0;
        public Calculator()
        {
        }

        internal long DoMath(string inputString)
        {
            string[] mathString = inputString
                .Replace("(", "( ")
                .Replace(")", " )")
                .Split(" ");

            string[] mathString2 = InsertBrackets(mathString);

            Console.WriteLine($"BEFORE: {inputString}");
            Console.WriteLine($"AFTER: {string.Join(" ", mathString2)}");

            return DoMath(mathString2);
        }

        private string[] InsertBrackets(string[] mathString)
        {
            string[] newMathString = (string[])mathString.Clone();

            int i = 0;
            while(i < newMathString.Length)
            {
                if (newMathString[i] == "+")
                {
                    int putOpenBracketBefore = GetPreviousIndex(newMathString, i);
                    int putCloseBracketAfter = GetNextIndex(newMathString, i);

                    string[] tmp = new string[newMathString.Length + 2];

                    Array.Copy(newMathString, 0, tmp, 0, putOpenBracketBefore);
                    tmp[putOpenBracketBefore] = "(";

                    Array.Copy(newMathString, putOpenBracketBefore, tmp, putOpenBracketBefore + 1, putCloseBracketAfter - putOpenBracketBefore + 1);
                    tmp[putCloseBracketAfter + 2] = ")";

                    if (newMathString.Length > putCloseBracketAfter + 1)
                    {
                        Array.Copy(newMathString, putCloseBracketAfter + 1, tmp, putCloseBracketAfter + 3, newMathString.Length - putCloseBracketAfter - 1);
                    }

                    newMathString = tmp;
                    i++;

                }
                i++;
            }
            return newMathString;
        }

        private int GetNextIndex(string[] newMathString, int i)
        {
            var numBrackets = 0;
            do
            {
                i++;

                switch (newMathString[i])
                {
                    case "(":
                        numBrackets++;
                        break;

                    case ")":
                        numBrackets--;
                        break;

                    default:
                        break;
                }

            } while (numBrackets != 0);

            return i;
        }

        private int GetPreviousIndex(string[] newMathString, int i)
        {
            var numBrackets = 0;
            do
            {
                i--;

                switch (newMathString[i])
                {
                    case "(":
                        numBrackets--;
                        break;

                    case ")":
                        numBrackets++;
                        break;

                    default:
                        break;
                }

            } while (numBrackets != 0);

            return i;
        }

        internal long DoMath_WithoutTree(string[] mathExpression)
        {
            long? result = null;
            string currentOperation = "";
            while(mathPointer < mathExpression.Length)
            {
                var m = mathExpression[mathPointer];
                switch (m)
                {
                    case "+":
                    case "-":
                    case "*":
                    case "/":
                        currentOperation = m;
                        mathPointer++;
                        break;
                    case "(":
                        mathPointer++;
                        var number = DoMath(mathExpression); 
                        if (!result.HasValue)
                        {
                            result = number;
                        }
                        else
                        {
                            result = Operate(result, currentOperation, number);
                        }
                        break;
                    case ")":
                        mathPointer++;
                        return result.Value;
                    default:
                        //OPERATE
                        long number2 = Convert.ToInt64(m);
                        if (!result.HasValue)
                        {
                            result = number2;
                        }
                        else
                        {
                            result = Operate(result, currentOperation, number2);
                        }
                        mathPointer++;
                        break;
                }
            }

            return result.Value;
        }

        internal long DoMath(string[] mathExpression)
        {
            MathNode root = CreateExpressionTree(mathExpression);

            Console.WriteLine(root);

            return root.Evaluate();
        }

        private Operator CreateExpressionTree(string[] mathExpression)
        {
            /*
            If the current token is a '(', add a new node as the left child of the current node, and descend to the left child.
            If the current token is in the list['+', '-', '/', '*'], set the root value of the current node to the operator represented by the current token.Add a new node as the right child of the current node and descend to the right child.
            If the current token is a number, set the root value of the current node to the number and return to the parent.
            If the current token is a ')', go to the parent of the current node.
            */

            Operand firstOperand = null;
            Operator currentOperator = null;

            while (mathPointer < mathExpression.Length)
            {
                var m = mathExpression[mathPointer];

                switch (m)
                {
                    case "+":
                    case "-":
                    case "*":
                    case "/":
                        if (currentOperator == null)
                        {
                            if (firstOperand != null)
                            {
                                currentOperator = new Operator(m, firstOperand);
                            }
                            else
                                throw new Exception("unexpected edge case: currentOperator is null and firstOperand is null");
                        }
                        else
                        {
                            currentOperator = new Operator(m, currentOperator);
                        }
                        mathPointer++;
                        break;

                    case "(":
                        mathPointer++;
                        var child2 = CreateExpressionTree(mathExpression);
                        if (currentOperator == null)
                            currentOperator = child2;
                        else
                            currentOperator.AddChild2(child2);
                        break;

                    case ")":
                        mathPointer++;
                        return currentOperator;

                    default: //must be a number
                        var operand = new Operand(Convert.ToInt32(m));

                        if (currentOperator == null)
                        {
                            if (firstOperand == null)
                                firstOperand = operand;
                            else
                                throw new Exception("unexpected edge case: currentOperator is null and firstOperand is already populated");
                        }                            
                        else
                            currentOperator.AddChild2(operand);

                        mathPointer++;
                        break;
                }

            }

            return currentOperator;
        }

        private static long? Operate(long? result, string m, long number)
        {
            switch (m)
            {
                case "+":
                    result += number;
                    break;
                case "-":
                    result -= number;
                    break;
                case "*":
                    result *= number;
                    break;
                case "/":
                    result /= number;
                    break;
            }

            return result;
        }

        private string[] ExtractBrackets(string[] mathString, int mathPointer)
        {
            List<string> brackets = new List<string>();

            for (int j = mathPointer+1; j < mathString.Length; j++)
            {
                if (mathString[mathPointer] == ")")
                {
                    return brackets.ToArray();
                }
                else
                {
                    brackets.Add(mathString[mathPointer]);
                }
            }

            throw new Exception("could not find )");
        }
    }
}