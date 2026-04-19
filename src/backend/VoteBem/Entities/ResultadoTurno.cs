namespace VoteBem.Entities
{
    public class ResultadoTurno
    {
        public long Sq_candidato { get; private set; }
        public long Cd_eleicao { get; private set; }
        public int Nr_turno { get; private set; }
        public int Nr_votos { get; private set; }
        public int? Cd_sit_tot_turno { get; private set; }
        public string? Ds_sit_tot_turno { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;
        public Eleicao Eleicao { get; private set; } = null!;

        // Pk -> sq_candidato + nr_turno

        protected ResultadoTurno() { }
    }
}
