namespace VoteBem.Entities
{
    public class ResumoProposta
    {
        public long IdResumo { get; private set; }
        public long SqCandidato { get; private set; }
        public string DsTema { get; private set; } = null!;
        public string TxResumo { get; private set; } = null!;
        public DateTime DtGeracao { get; private set; }

        public PropostaGoverno PropostaGoverno { get; private set; } = null!;

        protected ResumoProposta() { }
    }
}
