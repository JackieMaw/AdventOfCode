using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class Day2Tests
    {
        [Test]
        public void Day2a()
        {
            var intCodeProgram = Helper.LoadFromFile("..\\..\\..\\InputData\\2019day2.txt");
            intCodeProgram[1] = 12;
            intCodeProgram[2] = 2;
            var output = new Computer().Execute(intCodeProgram);            
            Assert.AreEqual(3706713, output);
        }

        [Test]
        public void Day2b()
        {
            var intCodeProgram = Helper.LoadFromFile("..\\..\\..\\InputData\\2019day2.txt");
            var outputToSeek = 19690720;
            var result = FindNounAndVerb(intCodeProgram, outputToSeek);          
            Assert.AreEqual(8609, result);
        }

        private static int FindNounAndVerb(long[] program, int outputToSeek)
        {
            for (int noun = 0; noun < 100; noun++)
            {
                for (int verb = 0; verb < 100; verb++)
                {
                    var thisProgram = (long[])program.Clone();

                    thisProgram[1] = noun;
                    thisProgram[2] = verb;

                    long answer = new Computer().Execute(thisProgram);

                    if (answer == outputToSeek)
                    {
                        return 100 * noun + verb;
                    }
                }
            }
            return -1;
        }
    }
}