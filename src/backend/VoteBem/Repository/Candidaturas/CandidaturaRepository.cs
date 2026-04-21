using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidaturas
{
    public class CandidaturaRepository(AppDbContext context) : ICandidaturaRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<(IEnumerable<Candidatura> candidaturas, int quantidadeCandidaturas)> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize)
        {
            var query = context.Candidaturas
                .Include(c => c.Partido)
                .AsNoTracking();

            var quantidadeCandidaturas = await query.CountAsync();

            var candidaturas = await query
                .OrderBy(c => c.NmUrnaCandidato)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (candidaturas, quantidadeCandidaturas);
        }
    }
}
