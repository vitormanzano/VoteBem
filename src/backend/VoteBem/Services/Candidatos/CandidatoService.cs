using VoteBem.Dtos.Candidatos;
using VoteBem.Dtos.Common;
using VoteBem.Entities;
using VoteBem.Mappers;
using VoteBem.Repository.Candidatos;

namespace VoteBem.Services.Candidatos
{
    public class CandidatoService(ICandidatoRepository candidatoRepository) : ICandidatoService
    {
        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetAllCandidatosPaginatedAsync(int pageNumber, int pageSize)
        {
            var (candidatos, total) = await candidatoRepository.GetAllCandidatosPaginatedAsync(pageNumber, pageSize);
            return BuildPagedResult(candidatos, pageNumber, pageSize, total);
        }

        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByNamePaginatedAsync(int pageNumber, int pageSize, string name)
        {
            if (string.IsNullOrEmpty(name))
                throw new ArgumentException("Nome não pode ser vazio!");

            var (candidatos, total) = await candidatoRepository.GetCandidatosByNamePaginatedAsync(pageNumber, pageSize, name.Trim());
            return BuildPagedResult(candidatos, pageNumber, pageSize, total);
        }

        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByPartidoPaginatedAsync(int pageNumber, int pageSize, string partido)
        {
            if (string.IsNullOrEmpty(partido))
                throw new ArgumentException("Partido não pode ser vazio!");

            var (candidatos, total) = await candidatoRepository.GetCandidatosByPartidoPaginatedAsync(pageNumber, pageSize, partido.Trim().ToUpper());
            return BuildPagedResult(candidatos, pageNumber, pageSize, total);
        }

        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByAnoEleitoralPaginatedAsync(int pageNumber, int pageSize, int ano)
        {
            if (ano != 2010 && ano != 2014 && ano != 2018 && ano != 2022)
                throw new ArgumentException("Ano eleitoral inválido! Os anos válidos são: 2010, 2014, 2018 e 2022.");

            var (candidatos, total) = await candidatoRepository.GetCandidatosByAnoEleitoralPaginatedAsync(pageNumber, pageSize, ano);
            return BuildPagedResult(candidatos, pageNumber, pageSize, total);
        }

        private static PagedResultDto<CandidatoPaginatedResponseDto> BuildPagedResult(IEnumerable<Candidato> candidatos, int pageNumber, int pageSize, int total)
        {
            var totalPages = (int)Math.Ceiling((double)total / pageSize);
            return new PagedResultDto<CandidatoPaginatedResponseDto>
            {
                Data = candidatos.Select(c => c.MapCandidatoParaCandidatoPaginatedResponseDto()),
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
