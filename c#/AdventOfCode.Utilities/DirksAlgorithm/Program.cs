using NUnit.Framework;
using System;
using System.Linq;

namespace DirksAlgorithm
{
    class Program
    {
        static void Main(string[] args)
        {
			TestCase1();
		}

		public static void TestCase1()
		{
			int start = 0;
			int[][][] edges = {
			new int[][] {new int[] {1, 7}},
			new int[][] {new int[] {2, 6}, new int[] {3, 20}, new int[] {4, 3}},
			new int[][] {new int[] {3, 14}},
			new int[][] {new int[] {4, 2}},
			new int[][] {},
			new int[][] {}
		};
			int?[] expected = { 0, 7, 13, 27, 10, null };
			int?[] actual = DijkstrasAlgorithm(start, edges);
			Assert.AreEqual(expected.Length, actual.Length);
			for (int i = 0; i < expected.Length; i++)
			{
				Assert.AreEqual(expected[i], actual[i]);
			}
		}
		public static int?[] DijkstrasAlgorithm(int start, int[][][] edges)
		{
			int numberOfVertices = edges.Length;

			//init as 0 = not visited yet
			bool[] visitedYet = new bool[numberOfVertices];
			int?[] allDistances = new int?[numberOfVertices];

			allDistances[start] = 0;
			Visit(start, visitedYet, allDistances, edges);			

			return allDistances;
		}

        private static void Visit(int currentVertex, bool[] visitedYet, int?[] allDistances, int[][][] edges)
        {
			if (visitedYet[currentVertex])
			{
				Console.WriteLine($"Skipping #{currentVertex}... ALREADY VISITED!");
				return;
			}

			Console.WriteLine($"Beginning Round for #{currentVertex}...");

            foreach (int[] pair in edges[currentVertex])
			{
				int vertex = pair[0];
				int distance = pair[1];

				int? currentTotalDistance = allDistances[vertex];
				int newTotalDistance = allDistances[currentVertex].Value + distance;

				if (!currentTotalDistance.HasValue || (newTotalDistance < currentTotalDistance.Value))
				{
					allDistances[vertex] = newTotalDistance;
					Console.WriteLine($"Shortest Distance to #{vertex} found via #{currentVertex} = {newTotalDistance}");
				}
			}

			visitedYet[currentVertex] = true;

            foreach (var pair in edges[currentVertex].Select(p => new { vertex = p[0], distance = p[1] }).OrderBy(p => p.distance))
            {
				Visit(pair.vertex, visitedYet, allDistances, edges);
            }
		}
    }
}