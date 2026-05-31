using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidatos
{
    public class CandidatoRepository(AppDbContext context) : ICandidatoRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<Candidato> GetCandidatoByNrCpfAsync(string nrCpf)
        {
            var candidato = await context.Candidatos
                .Where(c => c.NrCpfCandidato.Equals(nrCpf))
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.Partido)
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.RedesSociais
                    .Where(rs => ! (rs.TipoRedeSocial.Equals("OUTRO")))
                    .OrderBy(rs => rs.TipoRedeSocial))
                .AsNoTracking()
                .FirstOrDefaultAsync(c => c.NrCpfCandidato == nrCpf);
            return candidato;
        }

        public async Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize)
        {
            var query = context.Candidatos
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.Partido)
                .AsNoTracking();

            return await PaginateAsync(query, pageNumber, pageSize);
        }

        public async Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByNamePaginatedAsync(int pageNumber, int pageSize, string name)
        {
            var pattern = $"%{name}%";
            var query = context.Candidatos
                .Where(c => EF.Functions.ILike(c.NmCandidato, pattern)
                         || EF.Functions.ILike(c.NmUrnaCandidato ?? string.Empty, pattern))
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.Partido)
                .AsNoTracking();

            return await PaginateAsync(query, pageNumber, pageSize);
        }

        public async Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByPartidoPaginatedAsync(int pageNumber, int pageSize, string partido)
        {
            var query = context.Candidatos
                .Where(c => c.Candidaturas.Any(ca => ca.Partido.SgPartido == partido))
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.Partido)
                .AsNoTracking();

            return await PaginateAsync(query, pageNumber, pageSize);
        }

        public async Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByAnoEleitoralPaginatedAsync(int pageNumber, int pageSize, int ano)
        {
            var cdEleicoes = context.Eleicoes
                .Where(e => e.AnoEleicao == ano)
                .Select(e => e.CdEleicao);

            var query = context.Candidatos
               .Where(c => c.Candidaturas.Any(ca => cdEleicoes.Contains(ca.CdEleicao)))
               .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                   .ThenInclude(ca => ca.Partido)
               .AsNoTracking();

            return await PaginateAsync(query, pageNumber, pageSize);
        }

        private static async Task<(IEnumerable<Candidato>, int)> PaginateAsync(IQueryable<Candidato> query, int pageNumber, int pageSize)
        {
            var total = await query.CountAsync();
            var items = await query
                .OrderBy(c => c.NmUrnaCandidato)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (items, total);
        }
    }
}
