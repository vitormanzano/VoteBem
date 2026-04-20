using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class ResumoPropostaConfiguration : IEntityTypeConfiguration<ResumoProposta>
    {
        public void Configure(EntityTypeBuilder<ResumoProposta> builder)
        {
            builder.ToTable("resumo_proposta");

            builder.HasKey(rp => rp.IdResumo);

            builder.Property(rp => rp.IdResumo)
                .HasColumnName("id_resumo")
                .UseIdentityAlwaysColumn();

            builder.Property(rp => rp.SqCandidato)
                .HasColumnName("sq_candidato")
                .IsRequired();

            builder.Property(rp => rp.DsTema)
                .HasColumnName("ds_tema")
                .IsRequired();

            builder.Property(rp => rp.TxResumo)
                .HasColumnName("tx_resumo")
                .IsRequired();

            builder.Property(rp => rp.DtGeracao)
                .HasColumnName("dt_geracao")
                .HasDefaultValueSql("CURRENT_TIMESTAMP");

            builder.HasOne(rp => rp.PropostaGoverno)
                .WithMany(pg => pg.ResumosProposta)
                .HasForeignKey(rp => rp.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
