using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.ResumosProposta
{
    public class ResumoPropostaRepository(AppDbContext context) : IResumoPropostaRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<IEnumerable<ResumoProposta>> GetResumosBySqCandidatoAsync(long sqCandidato)
        {
            return await context.ResumosProposta
                .Where(rp => rp.SqCandidato == sqCandidato)
                .OrderBy(rp => rp.DsTema)
                .AsNoTracking()
                .ToListAsync();
        }

        public async Task<PropostaGoverno?> GetPropostaGovernoAsync(long sqCandidato)
        {
            return await context.PropostasGoverno
                .Where(pg => pg.SqCandidato == sqCandidato)
                .AsNoTracking()
                .FirstOrDefaultAsync();
        }
    }
}
