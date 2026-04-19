namespace VoteBem.Entities
{
    public class ResumoProposta
    {
        public long Id_resumo { get; private set; }
        public long Sq_candidato { get; private set; }
        public string Ds_tema { get; private set; } = null!;
        public string Tx_resumo { get; private set; } = null!;
        public DateTime Dt_geracao { get; private set; }

        public PropostaGoverno PropostaGoverno { get; private set; } = null!;

        protected ResumoProposta() { }
    }
}
