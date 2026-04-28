using VoteBem.Dtos.Candidaturas;
using VoteBem.Dtos.Common;
using VoteBem.Dtos.RedesSociais;
using VoteBem.Entities;
using VoteBem.Mappers;
using VoteBem.Repository.RedesSociais;

namespace VoteBem.Services.RedesSociais
{
    public class RedeSocialService(IRedeSocialRepository redeSocialRepository) : IRedeSocialService
    {
        public async Task<PagedResultDto<RedeSocialResponseDto>> GetAllBySqCandidatoPaginatedAsync(long sqCandidato, int pageNumber, int pageSize)
        {
            var (redesSociais, total) = await redeSocialRepository.GetRedesSociaisBySqCandidatoPaginatedAsync(sqCandidato, pageNumber, pageSize);

            return BuildPagedResult(redesSociais, pageNumber, pageSize, total);
        }

        private static PagedResultDto<RedeSocialResponseDto> BuildPagedResult(IEnumerable<RedeSocial> redesSociais, int pageNumber, int pageSize, int total)
        {
            var totalPages = (int)Math.Ceiling((double)total / pageSize);
            return new PagedResultDto<RedeSocialResponseDto>
            {
                Data = redesSociais.Select(rs => rs.MapRedeSocialToRedeSocialResponseDto()),
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
