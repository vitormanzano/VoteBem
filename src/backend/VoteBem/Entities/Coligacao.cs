namespace VoteBem.Entities
{
    public class Coligacao
    {
        public long Sq_coligacao { get; private set; }
        public long Cd_eleicao { get; private set; }
        public int Nr_turno { get; private set; }
        public string? Nm_coligacao { get; private set; }
        public string? Ds_composicao_coligacao { get; private set; }
        public string? Tp_agremiacao { get; private set; }
        public string? Sg_uf { get; private set; }

        public Eleicao Eleicao { get; private set; } = null!;

        protected Coligacao() { }
    }
}
