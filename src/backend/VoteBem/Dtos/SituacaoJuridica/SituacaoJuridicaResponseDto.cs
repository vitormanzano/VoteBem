namespace VoteBem.Dtos.SituacaoJuridica
{
    public record SituacaoJuridicaResponseDto
        (
            IEnumerable<CertidaoCriminalResponseDto> CertidoesCriminais,
            IEnumerable<MotivoCassacaoResponseDto> MotivosCassacao
        );
}
