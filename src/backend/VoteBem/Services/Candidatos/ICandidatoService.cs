using VoteBem.Dtos.Common;
using VoteBem.Dtos.Candidatos;

namespace VoteBem.Services.Candidatos
{
    public interface ICandidatoService
    {
        Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize);
        Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByNamePaginatedAsync(int pageNumber, int pageSize, string name);
        Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByPartidoPaginatedAsync(int pageNumber, int pageSize, string partido);
        Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByAnoEleitoralPaginatedAsync(int pageNumber, int pageSize, int ano);
    }
}
