namespace VoteBem.Entities
{
    public class CertidaoCriminal
    {
        public long Id_certidao { get; private set; }
        public long Sq_candidato { get; private set; }
        public string Nm_arquivo { get; private set; } = null!;
        public string? Ds_caminho_arquivo { get; private set; }
        public DateOnly? Dt_emissao { get; private set; }
        public DateOnly? Dt_validade { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;

        protected CertidaoCriminal() { }
    }
}
