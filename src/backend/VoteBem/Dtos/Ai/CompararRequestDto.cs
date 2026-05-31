namespace VoteBem.Dtos.Ai
{
    public record CompararRequestDto
    {
        public IEnumerable<long> SqCandidatos { get; set; } = [];
        public IEnumerable<string>? Temas { get; set; }
    }
}
