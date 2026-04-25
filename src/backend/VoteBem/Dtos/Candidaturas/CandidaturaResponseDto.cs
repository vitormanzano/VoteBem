namespace VoteBem.Dtos.Candidaturas
{
    public record CandidaturaResponseDto
        (
            long SqCandidato,
            int AnoEleicao,
            string NmUrnaCandidato,
            string DsCargo,
            string SgUf,
            int? NrCandidato,
            string DsSituacaoCandidatura,
            string DsOcupacao,
            string StReeleicao,
            decimal? VrDespesaMaxCampanha
        );
}
