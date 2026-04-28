using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.SituacaoJuridica
{
    public class SituacaoJuridicaRepository(AppDbContext context) : ISituacaoJuridicaRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<IEnumerable<CertidaoCriminal>> GetCertidoesCriminaisBySqCandidatoAsync(long sqCandidato)
        {
            return await context.CertidoesCriminais
                .Where(cc => cc.SqCandidato == sqCandidato)
                .AsNoTracking()
                .ToListAsync();
        }

        public async Task<IEnumerable<MotivoCassacao>> GetMotivosCassacaoBySqCandidatoAsync(long sqCandidato)
        {
            return await context.MotivosCassacao
                .Where(mc => mc.SqCandidato == sqCandidato)
                .AsNoTracking()
                .ToListAsync();
        }
    }
}
