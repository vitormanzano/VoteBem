namespace VoteBem.Dtos.BensCandidato
{
    public record BemCandidatoResponseDto
        (
            long SqCandidato,
            string? DsBem,
            string? DsTipoBem,
            string? VrBem,
            int? NrOrdem
        );
}
