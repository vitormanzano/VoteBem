namespace VoteBem.Dtos.Ai
{
    public record PropostaGovernoDto(
        long SqCandidato,
        string? NmArquivo,
        string? DsCaminhoArquivo,
        bool StProcessado
    );
}
