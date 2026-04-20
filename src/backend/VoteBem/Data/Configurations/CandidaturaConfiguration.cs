using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class CandidaturaConfiguration : IEntityTypeConfiguration<Candidatura>
    {
        public void Configure(EntityTypeBuilder<Candidatura> builder)
        {
            builder.ToTable("candidatura");

            builder.HasKey(ca => ca.SqCandidato);

            builder.Property(ca => ca.SqCandidato)
                .HasColumnName("sq_candidato")
                .IsRequired();

            builder.Property(ca => ca.NrCpfCandidato)
                .HasColumnName("nr_cpf_candidato")
                .HasMaxLength(11)
                .IsRequired();

            builder.Property(ca => ca.CdEleicao)
                .HasColumnName("cd_eleicao")
                .IsRequired();

            builder.Property(ca => ca.NrPartido)
                .HasColumnName("nr_partido");

            builder.Property(ca => ca.SqColigacao)
                .HasColumnName("sq_coligacao");

            builder.Property(ca => ca.NmUrnaCandidato)
                .HasColumnName("nm_urna_candidato");

            builder.Property(ca => ca.CdCargo)
                .HasColumnName("cd_cargo");

            builder.Property(ca => ca.DsCargo)
                .HasColumnName("ds_cargo");

            builder.Property(ca => ca.SgUf)
                .HasColumnName("sg_uf")
                .HasMaxLength(2);

            builder.Property(ca => ca.NrCandidato)
                .HasColumnName("nr_candidato");

            builder.Property(ca => ca.CdSituacaoCandidatura)
                .HasColumnName("cd_situacao_candidatura");

            builder.Property(ca => ca.DsSituacaoCandidatura)
                .HasColumnName("ds_situacao_candidatura");

            builder.Property(ca => ca.CdOcupacao)
                .HasColumnName("cd_ocupacao");

            builder.Property(ca => ca.DsOcupacao)
                .HasColumnName("ds_ocupacao");  

            builder.Property(ca => ca.FotoUrl)
                .HasColumnName("foto_url");

            builder.Property(ca => ca.StReeleicao)
                .HasColumnName("st_reeleicao")
                .HasMaxLength(1);

            builder.Property(ca => ca.VrDespesaMaxCampanha)
                .HasColumnName("vr_despesa_max_campanha")
                .HasColumnType("DECIMAL(15,2)");
             
            builder.HasOne(ca => ca.Candidato)
                .WithMany(c => c.Candidaturas)
                .HasForeignKey(ca => ca.NrCpfCandidato)
                .OnDelete(DeleteBehavior.Cascade);

            builder.HasOne(ca => ca.Partido)
                .WithMany(p => p.Candidaturas)
                .HasForeignKey(ca => ca.NrPartido);

            builder.HasOne(ca => ca.Coligacao)
                .WithMany(col => col.Candidaturas)
                .HasForeignKey(ca => ca.SqColigacao);      
        }
    }
}
