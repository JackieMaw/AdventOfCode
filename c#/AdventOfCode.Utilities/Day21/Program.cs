using AdventOfCode.Utilities;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Day21
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("How many times do any of those ingredients appear?");
            long answer = GetNumberOfNonAllergenic(ReadInput.GetStrings("Input.txt"));

            Console.WriteLine($"answer={answer}");

            Console.WriteLine("All Done!");
        }

        private static long GetNumberOfNonAllergenic(string[] inputStrings)
        {
            (var allPossibleTranslations, var allIngredients) = GetAllPossibleTranslations(inputStrings);
            (var translationsFromAllergen, var translationsFromIngredient) = GetActualTranslations(allPossibleTranslations);

            long nonAllergens = 0;
            foreach (var ingredient in allIngredients)
            {
                if (!translationsFromIngredient.ContainsKey(ingredient))
                    nonAllergens++;
            }

            var orderedByAllergen = translationsFromAllergen.OrderBy(pair => pair.Key);
            Console.WriteLine(string.Join(",", orderedByAllergen.Select(pair => pair.Key)));
            Console.WriteLine(string.Join(",", orderedByAllergen.Select(pair => pair.Value)));

            return nonAllergens;
        }

        private static (Dictionary<string, string>, Dictionary<string, string>) GetActualTranslations(Dictionary<string, List<string>> allPossibleTranslations)
        {
            var translationsFromAllergen = new Dictionary<string, string>();
            var translationsFromIngredient = new Dictionary<string, string>();

            while (allPossibleTranslations.Any())
            {
                foreach ((var allergen, var possibleTranslations) in allPossibleTranslations)
                {
                    if (possibleTranslations.Count() == 1)
                    {
                        string ingredient = possibleTranslations[0];
                        Console.WriteLine($"{allergen} ==> {ingredient}");
                        translationsFromAllergen[allergen] = ingredient;
                        translationsFromIngredient[ingredient] = allergen;
                    }
                    else
                    {
                        foreach (var translation in translationsFromAllergen.Values)
                        {
                            if (possibleTranslations.Contains(translation))
                            {
                                possibleTranslations.Remove(translation);
                                Console.WriteLine($"{allergen} has {possibleTranslations.Count()} possible translations.");
                            }
                        }
                    }
                }

                //mop up
                foreach (var allergen in translationsFromAllergen.Keys)
                {
                    allPossibleTranslations.Remove(allergen);
                }
            }

            return (translationsFromAllergen, translationsFromIngredient);
        }

        private static (Dictionary<string, List<string>>, List<string>) GetAllPossibleTranslations(string[] inputStrings)
        {
            var allPossibleTranslations = new Dictionary<string, List<string>>();
            var allIngredients = new List<string>();

            foreach (var input in inputStrings)
            {
                //mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
                var inputParts = input.Split("(");

                var ingredients = inputParts[0].Trim().Split(" ");

                var allergens = inputParts[1].Trim().Replace("contains ", "").Replace(")", "").Split(", ");

                foreach (var allergen in allergens)
                {
                    if (allPossibleTranslations.TryGetValue(allergen, out var possibleTranslations))
                    {
                        allPossibleTranslations[allergen] = ingredients.Intersect(possibleTranslations).ToList();
                        Console.WriteLine($"{allergen} has {allPossibleTranslations[allergen].Count()} possible translations.");
                    }
                    else
                    {
                        allPossibleTranslations[allergen] = ingredients.ToList();
                        Console.WriteLine($"{allergen} has {allPossibleTranslations[allergen].Count()} possible translations.");
                    }
                }

                allIngredients.AddRange(ingredients);
            }

            return (allPossibleTranslations, allIngredients);
        }
    }
}
