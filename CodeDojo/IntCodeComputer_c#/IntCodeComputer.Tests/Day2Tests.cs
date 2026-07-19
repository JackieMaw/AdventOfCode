using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class Day2Tests
    {
        [Test]
        public void Day2a()
        {
            var intCodeProgram = Helper.LoadIntsFromFile(@"C:\Work\AdventOfCode\Data\2019\input\input_2019_2_intcode_python.txt");
            intCodeProgram[1] = 12;
            intCodeProgram[2] = 2;
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(3706713, output);
        }

        [Test]
        public void Day2b()
        {
            var intCodeProgram = Helper.LoadIntsFromFile(@"C:\Work\AdventOfCode\Data\2019\input\input_2019_2_intcode_python.txt");
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(8609, output);
        }
    }
}
