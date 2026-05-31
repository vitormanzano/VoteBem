namespace VoteBem.Dtos.Ai
{
    public record ResumoPropostaDto
    {
        public long IdResumo { get; set; }
        public long SqCandidato { get; set; }
        public string DsTema { get; set; } = string.Empty;
        public string TxResumo { get; set; } = string.Empty;
        public DateTime DtGeracao { get; set; }
    }
}
