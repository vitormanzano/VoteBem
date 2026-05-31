using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class CertidaoCriminalConfiguration : IEntityTypeConfiguration<CertidaoCriminal>
    {
        public void Configure(EntityTypeBuilder<CertidaoCriminal> builder)
        {
            builder.ToTable("certidao_criminal");

            builder.HasKey(cc => cc.IdCertidao);

            builder.Property(cc => cc.IdCertidao)
                .HasColumnName("id_certidao");

            builder.Property(cc => cc.SqCandidato)
                .HasColumnName("sq_candidato")
                .IsRequired();

            builder.Property(cc => cc.NmArquivo)
                .HasColumnName("nm_arquivo")
                .IsRequired();

            builder.Property(cc => cc.DsCaminhoArquivo)
                .HasColumnName("ds_caminho_arquivo");

            builder.Property(cc => cc.DtEmissao)
                .HasColumnName("dt_emissao");

            builder.Property(cc => cc.DtValidade)
                .HasColumnName("dt_validade");

            builder.HasOne(cc => cc.Candidatura)
                .WithMany(c => c.CertidoesCriminais)
                .HasForeignKey(cc => cc.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
