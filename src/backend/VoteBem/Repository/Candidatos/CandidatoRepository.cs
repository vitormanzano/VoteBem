using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.Candidatos
{
    public class CandidatoRepository(AppDbContext context) : ICandidatoRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public async Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize)
        {
            var query = context.Candidatos
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.Partido)
                .AsNoTracking();

            var quantidadeCandidatos = await query.CountAsync();

            var candidatos = await query
                .OrderBy(c => c.NmUrnaCandidato)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (candidatos, quantidadeCandidatos);
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

            var quantidadeCandidatos = await query.CountAsync();

            var candidatos = await query
                .OrderBy(c => c.NmUrnaCandidato)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (candidatos, quantidadeCandidatos);
        }

        public async Task<(IEnumerable<Candidato> candidatos, int quantidadeCandidatos)> GetCandidatosByPartidoPaginatedAsync(int pageNumber, int pageSize, string partido)
        {
            var query = context.Candidatos
                .Where(c => c.Candidaturas.Any(ca => ca.Partido.SgPartido == partido))
                .Include(c => c.Candidaturas.OrderByDescending(ca => ca.CdEleicao).Take(1))
                    .ThenInclude(ca => ca.Partido)
                .AsNoTracking();

            var quantidadeCandidatos = await query.CountAsync();

            var candidatos = await query
                .OrderBy(c => c.NmUrnaCandidato)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (candidatos, quantidadeCandidatos); ;
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

            var quantidadeCandidatos = await query.CountAsync();

            var candidatos = await query
                .OrderBy(c => c.NmUrnaCandidato)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (candidatos, quantidadeCandidatos); ;
        }
    }
}
