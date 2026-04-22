using System.Globalization;
using VoteBem.Dtos.Candidatos;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class CandidatoMapper
    {
        private static readonly TextInfo TextInfo = CultureInfo.GetCultureInfo("pt-BR").TextInfo;

        public static CandidatoPaginatedResponseDto MapCandidatoParaCandidatoPaginatedResponseDto(this Candidato candidato)
        {
            var ultimaCandidatura = candidato.Candidaturas.FirstOrDefault();
            var nome = TextInfo.ToTitleCase((candidato.NmUrnaCandidato ?? candidato.NmCandidato).ToLower());
            return new CandidatoPaginatedResponseDto(
                nome,
                ultimaCandidatura?.Partido?.SgPartido ?? "Dado não disponível",
                ultimaCandidatura?.DsCargo ?? "Dado não disponível"
            );
        }
    }
}
