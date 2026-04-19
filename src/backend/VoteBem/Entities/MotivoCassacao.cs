namespace VoteBem.Entities
{
    public class MotivoCassacao
    {
        public long Sq_candidato { get; private set; }
        public string? Ds_tp_motivo { get; private set; }
        public string Ds_motivo { get; private set; } = null!;

        public Candidatura Candidatura { get; private set; } = null!;
        // Pk -> sq_candidato + ds_motivo

        protected MotivoCassacao() { }
    }
}
