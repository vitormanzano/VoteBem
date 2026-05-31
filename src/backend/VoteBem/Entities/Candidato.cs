namespace VoteBem.Entities
{
    public class Candidato
    {
        public string NrCpfCandidato { get; private set; } = null!;
        public string NmCandidato { get; private set; } = null!;
        public string? NmSocialCandidato { get; private set; }
        public string? NmUrnaCandidato { get; private set; }
        public DateOnly? DtNascimento { get; private set; }
        public string? SgUfNascimento { get; private set; }
        public int? CdGenero { get; private set; }
        public string? DsGenero { get; private set; }
        public int? CdGrauInstrucao { get; private set; }
        public string? DsGrauInstrucao { get; private set; }
        public int? CdEstadoCivil { get; private set; }
        public string? DsEstadoCivil { get; private set; }
        public int? CdCorRaca { get; private set; }
        public string? DsCorRaca { get; private set; }

        public ICollection<Candidatura> Candidaturas { get; private set; } = [];

        protected Candidato() { }
    }
}
