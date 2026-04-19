namespace VoteBem.Entities
{
    public class DespesaCandidato
    {
        public long Id_despesa { get; private set; }
        public long Sq_candidato { get; private set; }
        public string? Nr_documento { get; private set; }
        public string? Cpf_cnpj_fornecedor { get; private set; }
        public string? Nm_fornecedor { get; private set; }
        public DateOnly? Dt_despesa { get; private set; }
        public decimal? Vr_despesa { get; private set; }
        public string? Ds_tipo_despesa { get; private set; }
        public string? Ds_fonte_recurso { get; private set; }
        public string? Ds_especie_recurso { get; private set; }
        public string? Ds_despesa { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;
        // Pk -> id_despesa

        protected DespesaCandidato() { }
    }
}
