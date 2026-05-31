using VoteBem.Dtos.RedesSociais;

namespace VoteBem.Dtos.Candidatos
{
    public record CandidatoProfileDto
        (
            long SqCandidato,
            string FotoUrl,
            string NomeCompleto,
            string NomeUrna,
            int? NrCandidato,
            List<RedeSocialResponseDto> RedesSociais,
            string Partido,
            string CargoDisputado,
            string SgUf,
            string GrauInstrucao,
            string OcupacaoDeclarada,
            string SituacaoCandidatura,
            DateOnly? DtNascimento,
            string? DsGenero,
            string? SgUfNascimento,
            string? DsEstadoCivil
        );
}
