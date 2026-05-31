using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class PartidoConfiguration : IEntityTypeConfiguration<Partido>
    {
        public void Configure(EntityTypeBuilder<Partido> builder)
        {
            builder.ToTable("partido");

            builder.HasKey(p => p.NrPartido);

            builder.Property(p => p.NrPartido)
                .HasColumnName("nr_partido");

            builder.Property(p => p.SgPartido)
                .HasColumnName("sg_partido")
                .HasMaxLength(20)
                .IsRequired();

            builder.Property(p => p.NmPartido)
                .HasColumnName("nm_partido")
                .IsRequired();
        }
    }
}
