using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidaturas
{
    public class CandidaturaRepository(AppDbContext context) : ICandidaturaRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<(IEnumerable<Candidatura> candidaturas, int quantidadeCandidaturas)> GetAllByCandidatoPaginatedAsync(int pageNumber, int pageSize, string nrCpfCandidato)
        {
            var candidaturas = await context.Candidaturas
                .Where(ca => ca.NrCpfCandidato == nrCpfCandidato)
                .Include(ca => ca.Partido)
                .AsNoTracking()
                .ToListAsync();

            return (candidaturas, candidaturas.Count);
        }

        public async Task<Dictionary<long, int>> GetAnosEleicaoAsync(IEnumerable<long> cdEleicoes)
        {
            return await context.Eleicoes
                .Where(e => cdEleicoes.Contains(e.CdEleicao))
                .GroupBy(e => e.CdEleicao)
                .ToDictionaryAsync(g => g.Key, g => g.First().AnoEleicao);
        }

    }
}
