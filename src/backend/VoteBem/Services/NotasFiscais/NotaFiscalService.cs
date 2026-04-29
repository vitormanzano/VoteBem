using VoteBem.Dtos.Common;
using VoteBem.Dtos.NotasFiscais;
using VoteBem.Mappers;
using VoteBem.Repository.NotasFiscais;

namespace VoteBem.Services.NotasFiscais
{
    public class NotaFiscalService(INotaFiscalRepository notaFiscalRepository) : INotaFiscalService
    {
        public async Task<PagedResultDto<NotaFiscalResponseDto>> GetNotasFiscaisBySqCandidatoAsync(long sqCandidato, int pageNumber, int pageSize)
        {
            var (notas, total) = await notaFiscalRepository.GetNotasFiscaisBySqCandidatoAsync(sqCandidato, pageNumber, pageSize);

            var totalPages = (int)Math.Ceiling((double)total / pageSize);
            return new PagedResultDto<NotaFiscalResponseDto>
            {
                Data = notas.Select(nf => nf.MapToNotaFiscalResponseDto()),
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
