using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.ResumosProposta
{
    public interface IResumoPropostaRepository
    {
        IUnitOfWork UnitOfWork { get; }
        Task<IEnumerable<ResumoProposta>> GetResumosBySqCandidatoAsync(long sqCandidato);
        Task<PropostaGoverno?> GetPropostaGovernoAsync(long sqCandidato);
    }
}
