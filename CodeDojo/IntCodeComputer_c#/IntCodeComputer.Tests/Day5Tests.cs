using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class Day5Tests
    {
        [Test]
        public void Day5a()
        {
            var intCodeProgram = Computer.LoadIntCodeProgram("..\\..\\..\\InputData\\2019day5.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(13933662, output);
        }

        [Test]
        public void Day5b()
        {
            var intCodeProgram = Computer.LoadIntCodeProgram("..\\..\\..\\InputData\\2019day5.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(2369720, output);
        }
    }
}