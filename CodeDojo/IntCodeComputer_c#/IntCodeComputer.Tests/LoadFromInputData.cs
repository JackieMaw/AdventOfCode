using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class LoadFromInputDataTests
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void Sample()
        {
            var expected = new int[] { 0, 5, 9999, 444 };
            var actual = Computer.LoadIntCodeProgram("0,5,9999,444");
            Assert.AreEqual(expected, actual);
        }
    }
}