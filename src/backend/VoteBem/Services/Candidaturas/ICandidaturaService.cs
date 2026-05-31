using VoteBem.Dtos.Candidaturas;
using VoteBem.Dtos.Common;

namespace VoteBem.Services.Candidaturas
{
    public interface ICandidaturaService
    {
        Task<PagedResultDto<CandidaturaResponseDto>> GetAllByCandidatoPaginatedAsync(int pageNumber, int pageSize, string nrCpfCandidato);
    }
}
