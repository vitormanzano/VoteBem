namespace VoteBem.Entities
{
    public class PropostaGoverno
    {
        public long Sq_candidato { get; private set; }
        public string? Nm_arquivo { get; private set; }
        public string? Ds_caminho_arquivo { get; private set; }
        public string? Tx_conteudo_extraido { get; private set; }
        public bool St_processado { get; private set; }
        public DateTime? Dt_processamento { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;

        protected PropostaGoverno() { }
    }
}
