namespace VoteBem.Dtos.Ai
{
    public record TemaComparadoDto
    {
        public string Tema { get; set; } = string.Empty;
        public string Texto { get; set; } = string.Empty;
        public IEnumerable<string> CandidatosSemProposta { get; set; } = [];
    }
}
