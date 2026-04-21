using VoteBem.Dtos.Common;
using VoteBem.Dtos.Candidaturas;

namespace VoteBem.Services.Candidatos
{
    public interface ICandidatoService
    {
        Task<PagedResultDto<CandidaturaPaginatedResponseDto>> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize);
    }
}
