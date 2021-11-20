using System;
using System.Collections.Generic;
using System.Linq;

namespace Day4
{
    internal class Passport
    {
        static string[] mandatoryFields = { "byr", "ecl", "eyr", "hcl", "hgt", "iyr", "pid" };
 
        private readonly List<Tuple<string, string>> credentials;
        public Passport(string credentialString)
        {
            string[] credentialParts = credentialString.Trim().Split(" ");
            credentials = new List<Tuple<string, string>>(); //tuples are shit

            foreach (var credential in credentialParts) //do this using linq
            {
                var parts = credential.Trim().Split(":");
                string key = parts[0];
                if (key != "cid")
                {
                    credentials.Add(new Tuple<string, string>(parts[0], parts[1]));
                }
            }
            credentials.Sort();
        }
        internal bool IsValid()
        {
            if (credentials.Count != mandatoryFields.Length)
                return false;

            for (int i = 0; i < mandatoryFields.Length; i++)
            {
                if (credentials[i].Item1 != mandatoryFields[i])
                    return false;
            }

            //byr (Birth Year) - four digits; at least 1920 and at most 2002.
            string byr = credentials[0].Item2; //this is super ugly
            if (!IsValidNumber(byr, 1920, 2002))
                return false;

            //ecl(Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            string ecl = credentials[1].Item2;
            if (!IsValidEyeColour(ecl))
                return false;

            //eyr(Expiration Year) - four digits; at least 2020 and at most 2030.
            string eyr = credentials[2].Item2;
            if (!IsValidNumber(eyr, 2020, 2030))
                return false;

            //hcl(Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            string hcl = credentials[3].Item2;
            if (!IsValidHairColour(hcl))
                return false;

            //hgt(Height) - a number followed by either cm or in:
            //If cm, the number must be at least 150 and at most 193.
            //If in, the number must be at least 59 and at most 76.
            string hgt = credentials[4].Item2;
            if (!IsValidHeight(hgt))
                return false;

            //iyr(Issue Year) - four digits; at least 2010 and at most 2020.
            string iyr = credentials[5].Item2;
            if (!IsValidNumber(iyr, 2010, 2020))
                return false;

            //pid(Passport ID) - a nine - digit number, including leading zeroes.
            string pid = credentials[6].Item2;
            if (!IsValidPassportId(pid))
                return false;

            //cid(Country ID) - ignored, missing or not.

            return true;
        }

        private bool IsValidHeight(string hgt)
        {
            //If cm, the number must be at least 150 and at most 193.
            //If in, the number must be at least 59 and at most 76.
            string measurement = hgt.Substring(hgt.Length - 2);
            string number = hgt.Substring(0, hgt.Length - 2);

            if (measurement == "cm")
            {
                if (IsValidNumber(number, 150, 193))
                    return true;
            }
            else if (measurement == "in")
            {
                if (IsValidNumber(number, 59, 76))
                    return true;
            }
            return false;
        }

        private bool IsValidHairColour(string hcl)
        {
            if (!(hcl.Length == 7))
                return false;

            if (!(hcl.StartsWith("#")))
                return false;

            foreach (var c in hcl.Substring(1, 6))
            {
                int ascii = (int)c;
                if (!((ascii >= 48 && ascii <= 57) || (ascii >= 97 && ascii <= 102))) //this is HORRIBLE
                    return false;
            }
            return true;
        }

        private bool IsValidEyeColour(string ecl)
        {
            string[] validEyeColours = { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" }; //hash set?

            if (validEyeColours.Contains(ecl))
                return true;

            return false;
        }

        private bool IsValidPassportId(string pid)
        {
            if (pid.Length != 9)
                return false;

            try
            {
                var pidInt = Convert.ToInt64(pid);
            }
            catch(Exception)
            {
                return false;
            }
            return true;
        }

        private bool IsValidNumber(string yearString, int min, int max)
        {
            try
            {
                int year = Convert.ToInt32(yearString);
                if (year >= min && year <= max)
                    return true;
            }
            catch (Exception)
            {
            }
            return false;
        }


    }
}