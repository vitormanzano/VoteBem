using System.Globalization;
using VoteBem.Dtos.BensCandidato;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class BemCandidatoMapper
    {
        public static BemCandidatoResponseDto MapToBemCandidatoResponseDto(this BemCandidato bemCandidato)
        {
            if (bemCandidato == null) return null;
            return new BemCandidatoResponseDto
            (
                bemCandidato.SqCandidato,
                bemCandidato.DsBem ?? "Dado não disponível",
                bemCandidato.DsTipoBem ?? "Dado não disponível",
                bemCandidato.VrBem.HasValue ? $"R${bemCandidato.VrBem.Value.ToString("N2", CultureInfo.GetCultureInfo("pt-BR"))}" : null,
                bemCandidato.NrOrdemBem
            );
        }
    }
}
