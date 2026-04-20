namespace VoteBem.Entities
{
    public class CertidaoCriminal
    {
        public long IdCertidao { get; private set; }
        public long SqCandidato { get; private set; }
        public string NmArquivo { get; private set; } = null!;
        public string? DsCaminhoArquivo { get; private set; }
        public DateOnly? DtEmissao { get; private set; }
        public DateOnly? DtValidade { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;

        protected CertidaoCriminal() { }
    }
}
