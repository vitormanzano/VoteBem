using VoteBem.Dtos.Common;
using VoteBem.Dtos.NotasFiscais;

namespace VoteBem.Services.NotasFiscais
{
    public interface INotaFiscalService
    {
        Task<PagedResultDto<NotaFiscalResponseDto>> GetNotasFiscaisBySqCandidatoAsync(long sqCandidato, int pageNumber, int pageSize);
    }
}
