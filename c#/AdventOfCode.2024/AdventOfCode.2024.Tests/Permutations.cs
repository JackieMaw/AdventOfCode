using System;
using System.Collections.Generic;
public static class PermutationGenerator<T>
{

    public static List<List<T>> GetPermutations(List<T> options, int numToGenerate)
    {
        if (numToGenerate == 1)
        {
            return options.Select(o => new List<T> { o }).ToList();
        }
        else
        {
            List<List<T>> childPermuations = GetPermutations(options, numToGenerate - 1);

            List<List<T>> allPermutations = new List<List<T>>();
            foreach (List<T> p in childPermuations)
            {
                foreach (var option in options)
                {
                    var fullPermutation = new List<T>{ option };
                    fullPermutation.AddRange(p);
                    allPermutations.Add(fullPermutation);
                }
            } 
            return allPermutations;                      
        }
    }   
}