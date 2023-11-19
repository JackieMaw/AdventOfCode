using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class Day2Tests
    {
        [Test]
        public void Day2a()
        {
            var intCodeProgram = Computer.LoadIntCodeProgram("..\\..\\..\\InputData\\2019day2.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(3706713, output);
        }

        [Test]
        public void Day2b()
        {
            var intCodeProgram = Computer.LoadIntCodeProgram("..\\..\\..\\InputData\\2019day2.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(8609, output);
        }
    }
}