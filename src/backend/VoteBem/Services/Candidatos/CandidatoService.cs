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

        public async Task<PagedResultDto<CandidatoPaginatedResponseDto>> GetCandidatosByAnoEleitoralPaginatedAsync(int pageNumber, int pageSize, int ano)
        {
            if (ano != 2010 && ano != 2014 && ano != 2018 && ano != 2022)
                throw new ArgumentException("Ano eleitoral inválido! Os anos válidos são: 2010, 2014, 2018 e 2022.");

            var (candidatos, quantidadeCandidatos) = await candidatoRepository.GetCandidatosByAnoEleitoralPaginatedAsync(pageNumber, pageSize, ano);

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
