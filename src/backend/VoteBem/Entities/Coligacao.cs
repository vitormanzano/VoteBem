namespace VoteBem.Entities
{
    public class Coligacao
    {
        public long SqColigacao { get; private set; }
        public long CdEleicao { get; private set; }
        public int NrTurno { get; private set; }
        public string? NmColigacao { get; private set; }
        public string? DsComposicaoColigacao { get; private set; }
        public string? TpAgremiacao { get; private set; }
        public string? SgUf { get; private set; }

        public Eleicao Eleicao { get; private set; } = null!;
        public ICollection<Candidatura> Candidaturas { get; private set; } = [];

        protected Coligacao() { }
    }
}
