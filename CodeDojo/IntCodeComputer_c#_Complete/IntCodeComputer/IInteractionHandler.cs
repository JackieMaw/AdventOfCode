namespace IntCodeComputer
{
    public interface IInteractionHandler
    {
        long GetNextInput();
        void SaveOutput(long output);
    }
}