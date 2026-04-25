using VoteBem.Dtos.Candidaturas;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class CandidaturaMapper
    {
        public static CandidaturaResponseDto MapToCandidaturaResponseDto(this Candidatura candidatura, int anoEleicao)
        {
            return new CandidaturaResponseDto(
                candidatura.SqCandidato,
                anoEleicao,
                candidatura.NmUrnaCandidato ?? "Dado não disponível!",
                candidatura.DsCargo ?? "Dado não disponível!",
                candidatura.SgUf ?? "Dado não disponível!",
                candidatura.NrCandidato,
                candidatura.DsSituacaoCandidatura ?? "Dado não disponível!",
                candidatura.DsOcupacao ?? "Dado não disponível!",
                candidatura.StReeleicao ?? "Dado não disponível!",
                candidatura.VrDespesaMaxCampanha
            );
        }

    }
}
