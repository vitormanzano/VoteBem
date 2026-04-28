using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.NotasFiscais
{
    public class NotaFiscalRepository(AppDbContext context) : INotaFiscalRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<(IEnumerable<NotaFiscal>, int)> GetNotasFiscaisBySqCandidatoAsync(long sqCandidato, int pageNumber, int pageSize)
        {
            var query = context.NotasFiscais
                .Where(nf => nf.SqCandidato == sqCandidato)
                .AsNoTracking();

            var total = await query.CountAsync();
            var items = await query
                .OrderByDescending(nf => nf.DtEmissao)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (items, total);
        }
    }
}
