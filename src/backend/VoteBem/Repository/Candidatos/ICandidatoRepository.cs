using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidatos
{
    public interface ICandidatoRepository
    {
        IUnitOfWork UnitOfWork { get; }
        Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize);
        Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByNamePaginatedAsync(int pageNumber, int pageSize, string name);
    }
}
