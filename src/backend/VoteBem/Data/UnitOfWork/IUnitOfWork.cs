namespace VoteBem.Data.UnitOfWork
{
    public interface IUnitOfWork
    {
        public Task<bool> CommitAsync();
    }
}
