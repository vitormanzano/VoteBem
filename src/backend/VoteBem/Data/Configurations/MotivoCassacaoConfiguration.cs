using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class MotivoCassacaoConfiguration : IEntityTypeConfiguration<MotivoCassacao>
    {
        public void Configure(EntityTypeBuilder<MotivoCassacao> builder)
        {
            builder.ToTable("motivo_cassacao");

            builder.HasKey(mc => new { mc.SqCandidato, mc.DsMotivo });

            builder.Property(mc => mc.SqCandidato)
                .HasColumnName("sq_candidato")
                .IsRequired();

            builder.Property(mc => mc.DsTpMotivo)
                .HasColumnName("ds_tp_motivo");

            builder.Property(mc => mc.DsMotivo)
                .HasColumnName("ds_motivo")
                .IsRequired();

            builder.HasOne(mc => mc.Candidatura)
                .WithMany(c => c.MotivosCassacao)
                .HasForeignKey(mc => mc.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
