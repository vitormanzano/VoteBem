using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class EleicaoConfiguration : IEntityTypeConfiguration<Eleicao>
    {
        public void Configure(EntityTypeBuilder<Eleicao> builder)
        {
            builder.ToTable("eleicao");

            builder.HasKey(e => new { e.CdEleicao, e.NrTurno });

            builder.Property(e => e.CdEleicao)
                .HasColumnName("cd_eleicao")
                .IsRequired();

            builder.Property(e => e.NrTurno)
                .HasColumnName("nr_turno")
                .IsRequired();

            builder.Property(e => e.AnoEleicao)
                .HasColumnName("ano_eleicao")
                .IsRequired();

            builder.Property(e => e.CdTipoEleicao)
                .HasColumnName("cd_tipo_eleicao");

            builder.Property(e => e.NmTipoEleicao)
                .HasColumnName("nm_tipo_eleicao");

            builder.Property(e => e.DsEleicao)
                .HasColumnName("ds_eleicao");

            builder.Property(e => e.DtEleicao)
                .HasColumnName("dt_eleicao");
        }
    }
}
