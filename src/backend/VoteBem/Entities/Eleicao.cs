namespace VoteBem.Entities
{
    public class Eleicao
    {
        public long Cd_eleicao { get; private set; }
        public int Nr_turno { get; private set; }
        public int Ano_eleicao { get; private set; }
        public int? Cd_tipo_eleicao { get; private set; }
        public string? Nm_tipo_eleicao { get; private set; }
        public string? Ds_eleicao { get; private set; }
        public DateOnly? Dt_eleicao { get; private set; }

        // Pk -> cd_eleicao + nr_turno

        protected Eleicao() { }
    }
}
