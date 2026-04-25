namespace VoteBem.Dtos.BensCandidato
{
    public record BemCandidatoResponseDto
        (
            long SqCandidato,
            string? DsBem,
            string? DsTipoBem,
            decimal? VrBem,
            int? NrOrdem
        );
}
