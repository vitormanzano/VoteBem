namespace VoteBem.Entities
{
    public class NotaFiscal
    {
        public long Id_nota { get; private set; }
        public long? Sq_candidato { get; private set; }
        public int Cd_eleicao { get; private set; }
        public int Nr_candidato { get; private set; }
        public string Sg_uf { get; private set; } = null!;
        public string? Nr_nota_fiscal { get; private set; }
        public string? Nr_serie { get; private set; }
        public string? Cpf_cnpj_emitente { get; private set; }
        public DateOnly? Dt_emissao { get; private set; }
        public decimal? Vr_nota_fiscal { get; private set; }
        public string? Nr_chave_acesso { get; private set; }
        public string? Nm_url_acesso { get; private set; }

        public Candidatura? Candidatura { get; private set; }

        protected NotaFiscal() { }
    }
}
