namespace VoteBem.Entities
{
    public class NotaFiscal
    {
        public long IdNota { get; private set; }
        public long? SqCandidato { get; private set; }
        public int CdEleicao { get; private set; }
        public int NrCandidato { get; private set; }
        public string SgUf { get; private set; } = null!;
        public string? NrNotaFiscal { get; private set; }
        public string? NrSerie { get; private set; }
        public string? CpfCnpjEmitente { get; private set; }
        public DateOnly? DtEmissao { get; private set; }
        public decimal? VrNotaFiscal { get; private set; }
        public string? NrChaveAcesso { get; private set; }
        public string? NmUrlAcesso { get; private set; }

        public Candidatura? Candidatura { get; private set; }

        protected NotaFiscal() { }
    }
}
