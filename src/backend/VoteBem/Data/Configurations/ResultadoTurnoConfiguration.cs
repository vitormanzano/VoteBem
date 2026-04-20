using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class ResultadoTurnoConfiguration : IEntityTypeConfiguration<ResultadoTurno>
    {
        public void Configure(EntityTypeBuilder<ResultadoTurno> builder)
        {
            builder.ToTable("resultado_turno");

            builder.HasKey(rt => new { rt.SqCandidato, rt.NrTurno });

            builder.Property(rt => rt.SqCandidato)
                .HasColumnName("sq_candidato");

            builder.Property(rt => rt.CdEleicao)
                .HasColumnName("cd_eleicao")
                .IsRequired();

            builder.Property(rt => rt.NrTurno)
                .HasColumnName("nr_turno")
                .IsRequired();

            builder.Property(rt => rt.NrVotos)
                .HasColumnName("nr_votos")
                .HasDefaultValue(0);

            builder.Property(rt => rt.CdSitTotTurno)
                .HasColumnName("cd_sit_tot_turno");

            builder.Property(rt => rt.DsSitTotTurno)
                .HasColumnName("ds_sit_tot_turno");

            builder.HasOne(rt => rt.Candidatura)
                .WithMany(c => c.ResultadosTurno)
                .HasForeignKey(rt => rt.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);

            builder.HasOne(rt => rt.Eleicao)
                .WithMany(e => e.ResultadosTurno)
                .HasForeignKey(rt => new { rt.CdEleicao, rt.NrTurno })
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
