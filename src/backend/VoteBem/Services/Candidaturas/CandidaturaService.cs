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

            var (candidaturas, total) = await candidaturaRepository.GetAllByCandidatoPaginatedAsync(pageNumber, pageSize, nrCpfCandidato.Trim());
            var anos = await candidaturaRepository.GetAnosEleicaoAsync(candidaturas.Select(ca => ca.CdEleicao));
            return BuildPagedResult(candidaturas, anos, pageNumber, pageSize, total);
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
