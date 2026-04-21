using VoteBem.Dtos.Candidaturas;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class CandidaturaMapper
    {
        public static CandidaturaPaginatedResponseDto MapCandidaturaParaCandidatoPaginatedResponseDto(this Candidatura candidatura)
        {
            return new CandidaturaPaginatedResponseDto(
                candidatura.NmUrnaCandidato ?? string.Empty,
                candidatura.Partido?.SgPartido ?? string.Empty,
                candidatura.DsCargo ?? string.Empty
            );
        }
    }
}
