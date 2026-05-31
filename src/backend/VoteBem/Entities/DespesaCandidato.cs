namespace VoteBem.Entities
{
    public class DespesaCandidato
    {
        public long IdDespesa { get; private set; }
        public long SqCandidato { get; private set; }
        public string? NrDocumento { get; private set; }
        public string? CpfCnpjFornecedor { get; private set; }
        public string? NmFornecedor { get; private set; }
        public DateOnly? DtDespesa { get; private set; }
        public decimal? VrDespesa { get; private set; }
        public string? DsTipoDespesa { get; private set; }
        public string? DsFonteRecurso { get; private set; }
        public string? DsEspecieRecurso { get; private set; }
        public string? DsDespesa { get; private set; }

        public Candidatura Candidatura { get; private set; } = null!;

        protected DespesaCandidato() { }
    }
}
