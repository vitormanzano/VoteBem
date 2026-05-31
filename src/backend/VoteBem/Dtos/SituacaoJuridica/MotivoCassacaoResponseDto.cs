namespace VoteBem.Dtos.SituacaoJuridica
{
    public record MotivoCassacaoResponseDto
        (
            long SqCandidato,
            string? DsTpMotivo,
            string DsMotivo
        );
}
