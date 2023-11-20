using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class Day9Tests
    {
        [Test]
        public void Day9a()
        {
            var intCodeProgram = Helper.LoadIntsFromFile("..\\..\\..\\InputData\\2019day9.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(13933662, output);
        }

        [Test]
        public void Day9b()
        {
            var intCodeProgram = Helper.LoadIntsFromFile("..\\..\\..\\InputData\\2019day9.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(2369720, output);
        }
    }
}