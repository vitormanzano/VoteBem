namespace VoteBem.Entities
{
    public class Candidatura
    {
        public long SqCandidato { get; private set; }
        public string NrCpfCandidato { get; private set; } = null!;
        public long CdEleicao { get; private set; }
        public int? NrPartido { get; private set; }
        public long? SqColigacao { get; private set; }
        public string? NmUrnaCandidato { get; private set; }
        public int? CdCargo { get; private set; }
        public string? DsCargo { get; private set; }
        public string? SgUf { get; private set; }
        public int? NrCandidato { get; private set; }
        public int? CdSituacaoCandidatura { get; private set; }
        public string? DsSituacaoCandidatura { get; private set; }
        public int? CdOcupacao { get; private set; }
        public string? DsOcupacao { get; private set; }
        public string? FotoUrl { get; private set; }
        public string? StReeleicao { get; private set; }
        public decimal? VrDespesaMaxCampanha { get; private set; }

        public Candidato Candidato { get; private set; } = null!;
        public Partido? Partido { get; private set; }
        public Coligacao? Coligacao { get; private set; }

        public ICollection<BemCandidato> BensCandidato { get; private set; } = [];
        public ICollection<RedeSocial> RedesSociais { get; private set; } = [];
        public ICollection<CertidaoCriminal> CertidoesCriminais { get; private set; } = [];
        public ICollection<DespesaCandidato> Despesas { get; private set; } = [];
        public ICollection<NotaFiscal> NotasFiscais { get; private set; } = [];
        public ICollection<ResultadoTurno> ResultadosTurno { get; private set; } = [];
        public ICollection<MotivoCassacao> MotivosCassacao { get; private set; } = [];
        public PropostaGoverno? PropostaGoverno { get; private set; }

        protected Candidatura() { }
    }
}
