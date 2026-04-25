using VoteBem.Dtos.RedesSociais;

namespace VoteBem.Dtos.Candidatos
{
    public record CandidatoProfileDto
        (
            string FotoUrl,
            string NomeCompleto,
            string NomeUrna,
            int? NrCandidato,
            List<RedeSocialResponseDto> RedesSociais,
            string Partido,
            string CargoDisputado,
            string UF,
            string GrauInstrucao,
            string OcupacaoDeclarada,
            string SituacaoCandidatura
        );
}
