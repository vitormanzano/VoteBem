using VoteBem.Dtos.Candidatos;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class CandidatoMapper
    {
        public static CandidatoPaginatedResponseDto MapCandidatoParaCandidatoPaginatedResponseDto(this Candidato candidato)
        {
            var ultimaCandidatura = candidato.Candidaturas.FirstOrDefault();
            return new CandidatoPaginatedResponseDto(
                candidato.NmUrnaCandidato ?? candidato.NmCandidato,
                ultimaCandidatura?.Partido?.SgPartido ?? "Dado não disponível",
                ultimaCandidatura?.DsCargo ?? "Dado não disponível"
            );
        }
    }
}
