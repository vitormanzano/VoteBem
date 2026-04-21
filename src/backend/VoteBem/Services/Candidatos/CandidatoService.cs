using VoteBem.Dtos.Candidaturas;
using VoteBem.Dtos.Common;
using VoteBem.Mappers;
using VoteBem.Repository.Candidaturas;

namespace VoteBem.Services.Candidatos
{
    public class CandidatoService(ICandidaturaRepository candidaturaRepository) : ICandidatoService
    {
        public async Task<PagedResultDto<CandidaturaPaginatedResponseDto>> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize)
        {
            var (candidaturas, quantidadeCandidaturas) = await candidaturaRepository.GetAllCandidatosPaginatedAsync(pageNumber, pageSize);

            var totalPages = (int)Math.Ceiling((double)quantidadeCandidaturas / pageSize);

            return new PagedResultDto<CandidaturaPaginatedResponseDto>
            {
                Data = candidaturas.Select(c => c.MapCandidaturaParaCandidatoPaginatedResponseDto()),
                Page = pageNumber,
                PageSize = pageSize,
                TotalItems = quantidadeCandidaturas,
                TotalPages = totalPages,
                HasPreviousPage = pageNumber > 1,
                HasNextPage = pageNumber < totalPages
            };
        }
    }
}
