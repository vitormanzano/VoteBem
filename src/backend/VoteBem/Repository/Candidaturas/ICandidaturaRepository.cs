using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidaturas
{
    public interface ICandidaturaRepository
    {
        IUnitOfWork UnitOfWork { get; }
        Task<(IEnumerable<Candidatura> candidaturas, int quantidadeCandidaturas)> GetAllByCandidatoPaginatedAsync(int pageNumber, int pageSize, string nrCpfCandidato);
        Task<Dictionary<long, int>> GetAnosEleicaoAsync(IEnumerable<long> cdEleicoes);
    }
}
