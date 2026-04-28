using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.NotasFiscais
{
    public interface INotaFiscalRepository
    {
        IUnitOfWork UnitOfWork { get; }

        Task<(IEnumerable<NotaFiscal>, int)> GetNotasFiscaisBySqCandidatoAsync(long sqCandidato, int pageNumber, int pageSize);
    }
}
