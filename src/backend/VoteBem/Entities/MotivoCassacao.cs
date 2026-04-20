namespace VoteBem.Entities
{
    public class MotivoCassacao
    {
        public long SqCandidato { get; private set; }
        public string? DsTpMotivo { get; private set; }
        public string DsMotivo { get; private set; } = null!;

        public Candidatura Candidatura { get; private set; } = null!;

        protected MotivoCassacao() { }
    }
}
