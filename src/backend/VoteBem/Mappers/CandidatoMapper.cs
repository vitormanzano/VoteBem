using System.Globalization;
using VoteBem.Dtos.Candidatos;
using VoteBem.Dtos.RedesSociais;
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
                candidato.NrCpfCandidato,
                nome,
                ultimaCandidatura?.Partido?.SgPartido ?? "Dado não disponível",
                ultimaCandidatura?.DsCargo ?? "Dado não disponível"
            );
        }

        public static CandidatoProfileDto MapCandidatoParaCandidatoProfileDto(this Candidato candidato)
        {
            var ultimaCandidatura = candidato.Candidaturas.FirstOrDefault();
            var nomeCompleto = TextInfo.ToTitleCase(candidato.NmCandidato.ToLower());
            var nomeUrna = TextInfo.ToTitleCase((candidato.NmUrnaCandidato ?? candidato.NmCandidato).ToLower());
            var partido = ultimaCandidatura?.Partido != null ? TextInfo.ToTitleCase(ultimaCandidatura.Partido.SgPartido.ToLower()) : "Dado não disponível";
            var cargoDisputado = ultimaCandidatura?.DsCargo != null ? TextInfo.ToTitleCase(ultimaCandidatura.DsCargo.ToLower()) : "Dado não disponível";
            var fotoUrl = ultimaCandidatura?.FotoUrl != null ? $"/storage/{ultimaCandidatura.FotoUrl}" : "Dado não disponível";

            return new CandidatoProfileDto(
                ultimaCandidatura.SqCandidato,
                fotoUrl,
                nomeCompleto,
                nomeUrna,
                ultimaCandidatura?.NrCandidato,
                ultimaCandidatura?.RedesSociais.Select(rs => new RedeSocialResponseDto(rs?.TipoRedeSocial, rs?.DsUrl)).ToList() ?? new List<RedeSocialResponseDto>(),
                partido,
                cargoDisputado,
                ultimaCandidatura?.SgUf ?? "Dado não disponível",
                candidato.DsGrauInstrucao ?? "Dado não disponível",
                ultimaCandidatura?.DsOcupacao ?? "Dado não disponível",
                ultimaCandidatura?.DsSituacaoCandidatura ?? "Dado não disponível"
            );
        }
    }
}
