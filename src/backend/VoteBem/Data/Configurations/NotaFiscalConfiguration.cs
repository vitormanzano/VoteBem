using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class NotaFiscalConfiguration : IEntityTypeConfiguration<NotaFiscal>
    {
        public void Configure(EntityTypeBuilder<NotaFiscal> builder)
        {
            builder.ToTable("nota_fiscal");

            builder.HasKey(nf => nf.IdNota);

            builder.Property(nf => nf.IdNota)
                .HasColumnName("id_nota")
                .UseIdentityAlwaysColumn();

            builder.Property(nf => nf.SqCandidato)
                .HasColumnName("sq_candidato");

            builder.Property(nf => nf.CdEleicao)
                .HasColumnName("cd_eleicao")
                .IsRequired();

            builder.Property(nf => nf.NrCandidato)
                .HasColumnName("nr_candidato")
                .IsRequired();

            builder.Property(nf => nf.SgUf)
                .HasColumnName("sg_uf")
                .HasMaxLength(2)
                .IsRequired();

            builder.Property(nf => nf.NrNotaFiscal)
                .HasColumnName("nr_nota_fiscal");

            builder.Property(nf => nf.NrSerie)
                .HasColumnName("nr_serie");

            builder.Property(nf => nf.CpfCnpjEmitente)
                .HasColumnName("cpf_cnpj_emitente");

            builder.Property(nf => nf.DtEmissao)
                .HasColumnName("dt_emissao");

            builder.Property(nf => nf.VrNotaFiscal)
                .HasColumnName("vr_nota_fiscal")
                .HasColumnType("DECIMAL(15,2)");

            builder.Property(nf => nf.NrChaveAcesso)
                .HasColumnName("nr_chave_acesso");

            builder.Property(nf => nf.NmUrlAcesso)
                .HasColumnName("nm_url_acesso");

            builder.HasIndex(nf => new { nf.CdEleicao, nf.NrCandidato, nf.SgUf, nf.NrNotaFiscal, nf.CpfCnpjEmitente })
                .IsUnique()
                .HasDatabaseName("uq_nota_fiscal");

            builder.HasOne(nf => nf.Candidatura)
                .WithMany(c => c.NotasFiscais)
                .HasForeignKey(nf => nf.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
