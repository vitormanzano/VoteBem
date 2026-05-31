namespace VoteBem.Entities
{
    public class Eleicao
    {
        public long CdEleicao { get; private set; }
        public int NrTurno { get; private set; }
        public int AnoEleicao { get; private set; }
        public int? CdTipoEleicao { get; private set; }
        public string? NmTipoEleicao { get; private set; }
        public string? DsEleicao { get; private set; }
        public DateOnly? DtEleicao { get; private set; }

        public ICollection<Coligacao> Coligacoes { get; private set; } = [];
        public ICollection<ResultadoTurno> ResultadosTurno { get; private set; } = [];

        protected Eleicao() { }
    }
}
