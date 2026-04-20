namespace VoteBem.Entities
{
    public class Partido
    {
        public int NrPartido { get; private set; }
        public string SgPartido { get; private set; } = null!;
        public string NmPartido { get; private set; } = null!;

        public ICollection<Candidatura> Candidaturas { get; private set; } = [];

        protected Partido() { }
    }
}
