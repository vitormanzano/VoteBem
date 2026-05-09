namespace VoteBem.Dtos.Ai
{
    public record CompararResponseDto
    {
        public IEnumerable<CandidatoComparadoDto> Candidatos { get; set; } = [];
        public IEnumerable<TemaComparadoDto> Comparacoes { get; set; } = [];
    }
}
