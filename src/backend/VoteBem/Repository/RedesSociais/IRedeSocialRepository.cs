using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.RedesSociais
{
    public interface IRedeSocialRepository
    {
        IUnitOfWork UnitOfWork { get; }
        Task<(IEnumerable<RedeSocial>, int)> GetRedesSociaisBySqCandidatoPaginatedAsync(long sqCandidato, int pageNumber, int pageSize);
    }
}
