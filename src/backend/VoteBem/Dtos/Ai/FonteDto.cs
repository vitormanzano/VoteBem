namespace VoteBem.Dtos.Ai
{
    public record FonteDto
    {
        public int? Ref { get; set; }
        public long? SqCandidato { get; set; }
        public string? Nome { get; set; }
        public int? Ano { get; set; }
        public string? Trecho { get; set; }
    }
}
