namespace VoteBem.Entities
{
    public class ResultadoTurno
    {
        public long SqCandidato { get; private set; }
        public long CdEleicao { get; private set; }
        public int NrTurno { get; private set; }
        public int NrVotos { get; private set; }
        public int? CdSitTotTurno { get; private set; }
        public string? DsSitTotTurno { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;
        public Eleicao Eleicao { get; private set; } = null!;

        protected ResultadoTurno() { }
    }
}
