using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidatos
{
    public interface ICandidatoRepository
    {
        IUnitOfWork UnitOfWork { get; }
        Task<Candidato> GetCandidatoByNrCpfAsync(string nrCpf);
        Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize);
        Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByNamePaginatedAsync(int pageNumber, int pageSize, string name);
        Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByPartidoPaginatedAsync(int pageNumber, int pageSize, string partido);
        Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByAnoEleitoralPaginatedAsync(int pageNumber, int pageSize, int ano);
    }
}
