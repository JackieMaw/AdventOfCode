using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Text;

namespace Day15
{
    [TestFixture]
    public class MyTests
    {
        [Test]
        public void Test1()
        {
            Assert.AreEqual(7, 7);
        }

        [Test]
        public void Test2()
        {
            Assert.AreEqual(7, 8);
        }
    }
}
