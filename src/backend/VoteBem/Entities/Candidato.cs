namespace VoteBem.Entities
{
    public class Candidato
    {
        public string Nr_cpf_candidato { get; private set; } = null!;
        public string Nm_candidato { get; private set; } = null!;
        public string? Nm_social_candidato { get; private set; }
        public string? Nm_urna_candidato { get; private set; }
        public DateOnly? Dt_nascimento { get; private set; }
        public string? Sg_uf_nascimento { get; private set; }
        public int? Cd_genero { get; private set; }
        public string? Ds_genero { get; private set; }
        public int? Cd_grau_instrucao { get; private set; }
        public string? Ds_grau_instrucao { get; private set; }
        public int? Cd_estado_civil { get; private set; }
        public string? Ds_estado_civil { get; private set; }
        public int? Cd_cor_raca { get; private set; }
        public string? Ds_cor_raca { get; private set; }

        protected Candidato() { }
    }
}
