using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.BensCadidato
{
    public interface IBemCandidatoRepository
    {
        IUnitOfWork UnitOfWork { get; }

        Task<IEnumerable<BemCandidato>> GetBensCandidatoBySqCandidatoAsync(long sqCandidato);
    }
}
