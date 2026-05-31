using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class BemCandidatoConfiguration : IEntityTypeConfiguration<BemCandidato>
    {
        public void Configure(EntityTypeBuilder<BemCandidato> builder)
        {
            builder.ToTable("bem_candidato");

            builder.HasKey(bc => new { bc.SqCandidato, bc.NrOrdemBem});

            builder.Property(bc => bc.SqCandidato)
                .HasColumnName("sq_candidato")
                .IsRequired();

            builder.Property(bc => bc.NrOrdemBem)
                .HasColumnName("nr_ordem_bem")
                .IsRequired();

            builder.Property(bc => bc.CdTipoBem)
                .HasColumnName("cd_tipo_bem");

            builder.Property(bc => bc.DsTipoBem)
                .HasColumnName("ds_tipo_bem");

            builder.Property(bc => bc.DsBem)
                .HasColumnName("ds_bem");

            builder.Property(bc => bc.VrBem)
                .HasColumnName("vr_bem")
                .HasColumnType("DECIMAL(15,2)");

            builder
                .HasOne(bc => bc.Candidatura)
                .WithMany(c => c.BensCandidato)
                .HasForeignKey(bc => bc.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
