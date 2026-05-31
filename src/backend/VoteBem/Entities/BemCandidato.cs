namespace VoteBem.Entities
{
    public class BemCandidato
    {
        public long SqCandidato { get; private set; }
        public int NrOrdemBem { get; private set; }
        public int? CdTipoBem { get; private set; }
        public string? DsTipoBem { get; private set; }
        public string? DsBem { get; private set; }
        public decimal? VrBem { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;

        protected BemCandidato() { }
    }
}
