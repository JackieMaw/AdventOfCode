interface IAoCSupplier
{
    string[] GetPuzzleInput(int year, int day, string suffix = "");
    string GetPuzzleInput_SingleLine(int year, int day, string suffix = "");
}