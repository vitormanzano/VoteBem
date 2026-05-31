using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class CandidatoConfiguration : IEntityTypeConfiguration<Candidato>
    {
        public void Configure(EntityTypeBuilder<Candidato> builder)
        {
            builder.ToTable("candidato");

              builder.HasKey(c => c.NrCpfCandidato);

            builder.Property(c => c.NrCpfCandidato)
                .HasColumnName("nr_cpf_candidato")
                .HasMaxLength(11)
                .IsRequired();

            builder.Property(c => c.NmCandidato)
                .HasColumnName("nm_candidato")
                .IsRequired();

            builder.Property(c => c.NmSocialCandidato)
                .HasColumnName("nm_social_candidato");

            builder.Property(c => c.NmUrnaCandidato)
                .HasColumnName("nm_urna_candidato");

            builder.Property(c => c.DtNascimento)
                .HasColumnName("dt_nascimento");

            builder.Property(c => c.SgUfNascimento)
                .HasColumnName("sg_uf_nascimento")
                .HasMaxLength(2);

            builder.Property(c => c.CdGenero)
                .HasColumnName("cd_genero");

            builder.Property(c => c.DsGenero)
                .HasColumnName("ds_genero");

            builder.Property(c => c.CdGrauInstrucao)
                .HasColumnName("cd_grau_instrucao");

            builder.Property(c => c.DsGrauInstrucao)
                .HasColumnName("ds_grau_instrucao");

            builder.Property(c => c.CdEstadoCivil)
                .HasColumnName("cd_estado_civil");

            builder.Property(c => c.DsEstadoCivil)
                .HasColumnName("ds_estado_civil");

            builder.Property(c => c.CdCorRaca)
                .HasColumnName("cd_cor_raca");

            builder.Property(c => c.DsCorRaca)
                .HasColumnName("ds_cor_raca");
        }
    }
}
