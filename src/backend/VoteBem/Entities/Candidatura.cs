namespace VoteBem.Entities
{
    public class Candidatura
    {
        public long Sq_candidato { get; private set; }
        public string Nr_cpf_candidato { get; private set; } = null!;
        public long Cd_eleicao { get; private set; }
        public int? Nr_partido { get; private set; }
        public long? Sq_coligacao { get; private set; }
        public string? Nm_urna_candidato { get; private set; }
        public int? Cd_cargo { get; private set; }
        public string? Ds_cargo { get; private set; }
        public string? Sg_uf { get; private set; }
        public int? Nr_candidato { get; private set; }
        public int? Cd_situacao_candidatura { get; private set; }
        public string? Ds_situacao_candidatura { get; private set; }
        public int? Cd_ocupacao { get; private set; }
        public string? Ds_ocupacao { get; private set; }
        public string? Foto_url { get; private set; }
        public string? St_reeleicao { get; private set; }
        public decimal? Vr_despesa_max_campanha { get; private set; }

        public Candidato Candidato { get; private set; } = null!;
        public Partido? Partido { get; private set; }
        public Coligacao? Coligacao { get; private set; }

        protected Candidatura() { }
    }
}
