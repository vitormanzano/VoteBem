using Microsoft.EntityFrameworkCore;
using VoteBem.Data;
using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.RedesSociais
{
    public class RedeSocialRepository(AppDbContext context) : IRedeSocialRepository
    {
        public IUnitOfWork UnitOfWork => context;

        public Task<(IEnumerable<RedeSocial>, int)> GetRedesSociaisBySqCandidatoPaginatedAsync(long sqCandidato, int pageNumber, int pageSize)
        {
            var query = context.RedesSociais
                .Where(rs => rs.SqCandidato == sqCandidato)
                .AsNoTracking();

            return PaginateAsync(query, pageNumber, pageSize);

        }

        private static async Task<(IEnumerable<RedeSocial>, int)> PaginateAsync(IQueryable<RedeSocial> query, int pageNumber, int pageSize)
        {
            var total = await query.CountAsync();
            var items = await query
                .OrderByDescending(rs => rs.NrOrdem)
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return (items, total);
        }
    }
}
