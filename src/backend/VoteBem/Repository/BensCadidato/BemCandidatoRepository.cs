using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.BensCadidato
{
    public class BemCandidatoRepository(AppDbContext context) : IBemCandidatoRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<IEnumerable<BemCandidato>> GetBensCandidatoBySqCandidatoAsync(long sqCandidato)
        {
            var bensCandidato = await context.BensCandidato
                .Where(bc => bc.SqCandidato == sqCandidato)
                .AsNoTracking()
                .ToListAsync();
            return bensCandidato;
        }
    }
}
