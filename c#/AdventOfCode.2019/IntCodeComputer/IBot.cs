namespace MyComputer
{
    public interface IBot
    {
        long GetNextInput();
        void SaveOutput(long output);
    }
}