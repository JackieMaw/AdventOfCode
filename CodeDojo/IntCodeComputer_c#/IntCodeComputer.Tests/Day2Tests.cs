using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class Day2Tests
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void FullInput()
        {
            var intCodeProgram = Computer.LoadIntCodeProgram(".\\InputData\\2019day2.txt");
            var output = new Computer().Execute(intCodeProgram);
        }
    }
}