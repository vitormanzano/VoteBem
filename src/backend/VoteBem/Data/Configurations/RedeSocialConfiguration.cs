using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class RedeSocialConfiguration : IEntityTypeConfiguration<RedeSocial>
    {
        public void Configure(EntityTypeBuilder<RedeSocial> builder)
        {
            builder.ToTable("rede_social");

            builder.HasKey(rs => new { rs.SqCandidato, rs.NrOrdem });

            builder.Property(rs => rs.SqCandidato)
                .HasColumnName("sq_candidato");

            builder.Property(rs => rs.NrOrdem)
                .HasColumnName("nr_ordem")
                .IsRequired();

            builder.Property(rs => rs.DsUrl)
                .HasColumnName("ds_url");

            builder.Property(rs => rs.TipoRedeSocial)
                .HasColumnName("tipo_rede_social");

            builder.HasOne(rs => rs.Candidatura)
                .WithMany(c => c.RedesSociais)
                .HasForeignKey(rs => rs.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
