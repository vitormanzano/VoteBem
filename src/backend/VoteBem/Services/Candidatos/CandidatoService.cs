using VoteBem.Dtos.Candidatos;
using VoteBem.Dtos.Common;
using VoteBem.Mappers;
using VoteBem.Repository.Candidatos;

namespace VoteBem.Services.Candidatos
{
    public class CandidatoService(ICandidatoRepository candidatoRepository) : ICandidatoService
    {
        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize)
        {
            var (candidatos, quantidadeCandidatos) = await candidatoRepository.GetAllCandidatosPaginatedAsync(pageNumber, pageSize);

            var totalPages = (int)Math.Ceiling((double)quantidadeCandidatos / pageSize);

            return new PagedResultDto<CandidatoPaginatedResponseDto>
            {
                Data = candidatos.Select(c => c.MapCandidatoParaCandidatoPaginatedResponseDto()),
                Page = pageNumber,
                PageSize = pageSize,
                TotalItems = quantidadeCandidatos,
                TotalPages = totalPages,
                HasPreviousPage = pageNumber > 1,
                HasNextPage = pageNumber < totalPages
            };
        }

        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByNamePaginatedAsync(int pageNumber, int pageSize, string name)
        {
            if (string.IsNullOrEmpty(name))
                throw new ArgumentException("Nome não pode ser vazio!");

            name = name.Trim();

            var (candidatos, quantidadeCandidatos) = await candidatoRepository.GetCandidatosByNamePaginatedAsync(pageNumber, pageSize, name);

            var totalPages = (int)Math.Ceiling((double)quantidadeCandidatos / pageSize);

            return new PagedResultDto<CandidatoPaginatedResponseDto>
            {
                Data = candidatos.Select(c => c.MapCandidatoParaCandidatoPaginatedResponseDto()),
                Page = pageNumber,
                PageSize = pageSize,
                TotalItems = quantidadeCandidatos,
                TotalPages = totalPages,
                HasPreviousPage = pageNumber > 1,
                HasNextPage = pageNumber < totalPages
            };
        }

        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByPartidoPaginatedAsync(int pageNumber, int pageSize, string partido)
        {
            if (string.IsNullOrEmpty(partido))
                throw new ArgumentException("Partido não pode ser vazio!");

            partido = partido.Trim().ToUpper();

            var (candidatos, quantidadeCandidatos) = await candidatoRepository.GetCandidatosByPartidoPaginatedAsync(pageNumber, pageSize, partido);   

            var totalPages = (int)Math.Ceiling((double)quantidadeCandidatos / pageSize);

            return new PagedResultDto<CandidatoPaginatedResponseDto>
            {
                Data = candidatos.Select(c => c.MapCandidatoParaCandidatoPaginatedResponseDto()),
                Page = pageNumber,
                PageSize = pageSize,
                TotalItems = quantidadeCandidatos,
                TotalPages = totalPages,
                HasPreviousPage = pageNumber > 1,
                HasNextPage = pageNumber < totalPages
            };
        }
    }
}
