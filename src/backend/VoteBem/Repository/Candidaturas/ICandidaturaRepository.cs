using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidaturas
{
    public interface ICandidaturaRepository
    {
        IUnitOfWork UnitOfWork { get; }
        Task<(IEnumerable<Candidatura> candidaturas, int quantidadeCandidaturas)> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize);
    }
}
