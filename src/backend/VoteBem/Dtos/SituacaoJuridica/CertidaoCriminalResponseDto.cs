namespace VoteBem.Dtos.SituacaoJuridica
{
    public record CertidaoCriminalResponseDto
        (
            long SqCandidato,
            string NmArquivo,
            string? DsCaminhoArquivo
        );
}
