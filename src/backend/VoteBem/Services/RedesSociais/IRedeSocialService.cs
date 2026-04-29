using VoteBem.Dtos.Common;
using VoteBem.Dtos.RedesSociais;

namespace VoteBem.Services.RedesSociais
{
    public interface IRedeSocialService
    {
        Task<PagedResultDto<RedeSocialResponseDto>> GetAllBySqCandidatoPaginatedAsync(long sqCandidato, int pageNumber, int pageSize);
    }
}
