using VoteBem.Dtos.Candidaturas;
using VoteBem.Dtos.Common;
using VoteBem.Entities;
using VoteBem.Mappers;
using VoteBem.Repository.Candidaturas;

namespace VoteBem.Services.Candidaturas
{
    public class CandidaturaService(ICandidaturaRepository candidaturaRepository) : ICandidaturaService
    {
        public async Task<PagedResultDto<CandidaturaResponseDto>> GetAllByCandidatoPaginatedAsync(int pageNumber, int pageSize, string nrCpfCandidato)
        {
            if (string.IsNullOrEmpty(nrCpfCandidato))
                throw new ArgumentException("CPF não pode ser vazio!");

            var (candidaturas, _) = await candidaturaRepository.GetAllByCandidatoPaginatedAsync(pageNumber, pageSize, nrCpfCandidato.Trim());
            var anos = await candidaturaRepository.GetAnosEleicaoAsync(candidaturas.Select(ca => ca.CdEleicao));

            // Turno 1 e turno 2 de um mesmo ano podem ter CdEleicao diferentes.
            // Mantém apenas o menor SQ por ano (turno 1), que é o que as propostas referenciam.
            var deduped = candidaturas
                .GroupBy(ca => anos.GetValueOrDefault(ca.CdEleicao))
                .Select(g => g.OrderBy(ca => ca.SqCandidato).First())
                .OrderByDescending(ca => anos.GetValueOrDefault(ca.CdEleicao))
                .ToList();

            var total = deduped.Count;
            var paged = deduped
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize);

            return BuildPagedResult(paged, anos, pageNumber, pageSize, total);
        }

        private static PagedResultDto<CandidaturaResponseDto> BuildPagedResult(IEnumerable<Candidatura> candidaturas, Dictionary<long, int> anos, int pageNumber, int pageSize, int total)
        {
            var totalPages = (int)Math.Ceiling((double)total / pageSize);
            return new PagedResultDto<CandidaturaResponseDto>
            {
                Data = candidaturas.Select(ca => ca.MapToCandidaturaResponseDto(anos.GetValueOrDefault(ca.CdEleicao))),
                Page = pageNumber,
                PageSize = pageSize,
                TotalItems = total,
                TotalPages = totalPages,
                HasPreviousPage = pageNumber > 1,
                HasNextPage = pageNumber < totalPages
            };
        }
    }
}
