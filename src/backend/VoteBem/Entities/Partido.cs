namespace VoteBem.Entities
{
    public class Partido
    {
        public int Nr_partido { get; private set; }
        public string Sg_partido { get; private set; } = null!;
        public string Nm_partido { get; private set; } = null!;

        protected Partido() { }
    }
}
