namespace VoteBem.Entities
{
    public class PropostaGoverno
    {
        public long SqCandidato { get; private set; }
        public string? NmArquivo { get; private set; }
        public string? DsCaminhoArquivo { get; private set; }
        public string? TxConteudoExtraido { get; private set; }
        public bool StProcessado { get; private set; }
        public DateTime? DtProcessamento { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;
        public ICollection<ResumoProposta> ResumosProposta { get; private set; } = [];

        protected PropostaGoverno() { }
    }
}
