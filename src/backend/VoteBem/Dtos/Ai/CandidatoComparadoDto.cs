namespace VoteBem.Dtos.Ai
{
    public record CandidatoComparadoDto
    {
        public long SqCandidato { get; set; }
        public string Nome { get; set; } = string.Empty;
        public int? Ano { get; set; }
        public IEnumerable<string> TemasDisponiveis { get; set; } = [];
    }
}
