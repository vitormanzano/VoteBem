namespace VoteBem.Dtos.Ai
{
    public record ChatResponseDto
    {
        public string Resposta { get; set; } = string.Empty;
        public IEnumerable<FonteDto> Fontes { get; set; } = [];
        public string? Categoria { get; set; }
    }
}
