namespace VoteBem.Entities
{
    public class RedeSocial
    {
        public long Sq_candidato { get; private set; }
        public int Nr_ordem { get; private set; }
        public string? Ds_url { get; private set; }
        public string? Tipo_rede_social { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;
        // Pk -> sq_candidato + nr_ordem

        protected RedeSocial() { }
    }
}
