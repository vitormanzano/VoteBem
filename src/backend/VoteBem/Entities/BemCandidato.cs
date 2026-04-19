namespace VoteBem.Entities
{
    public class BemCandidato
    {
        public long Sq_candidato { get; private set; }
        public int Nr_ordem_bem { get; private set; }
        public int? Cd_tipo_bem { get; private set; }
        public string? Ds_tipo_bem { get; private set; }
        public string? Ds_bem { get; private set; }
        public decimal? Vr_bem { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;
        // Pk -> sq_candidato + nr_ordem_bem

        protected BemCandidato() { }
    }
}
