namespace VoteBem.Entities
{
    public class RedeSocial
    {
        public long SqCandidato { get; private set; }
        public int NrOrdem { get; private set; }
        public string? DsUrl { get; private set; }
        public string? TipoRedeSocial { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;

        protected RedeSocial() { }
    }
}
