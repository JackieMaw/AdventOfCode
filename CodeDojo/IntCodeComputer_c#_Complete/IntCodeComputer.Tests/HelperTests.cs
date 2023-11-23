using NUnit.Framework;
using IntCodeComputer;

namespace Tests
{
    public class HelperTests
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void Sample()
        {
            var expected = new int[] { 0, 5, 9999, 444 };
            var actual = Helper.LoadFromString("0,5,9999,444");
            Assert.AreEqual(expected, actual);
        }
    }
}