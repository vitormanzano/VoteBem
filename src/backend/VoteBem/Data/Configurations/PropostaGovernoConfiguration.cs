using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class PropostaGovernoConfiguration : IEntityTypeConfiguration<PropostaGoverno>
    {
        public void Configure(EntityTypeBuilder<PropostaGoverno> builder)
        {
            builder.ToTable("proposta_governo");

            builder.HasKey(pg => pg.SqCandidato);

            builder.Property(pg => pg.SqCandidato)
                .HasColumnName("sq_candidato");

            builder.Property(pg => pg.NmArquivo)
                .HasColumnName("nm_arquivo");

            builder.Property(pg => pg.DsCaminhoArquivo)
                .HasColumnName("ds_caminho_arquivo");

            builder.Property(pg => pg.TxConteudoExtraido)
                .HasColumnName("tx_conteudo_extraido");

            builder.Property(pg => pg.StProcessado)
                .HasColumnName("st_processado")
                .HasDefaultValue(false);

            builder.Property(pg => pg.DtProcessamento)
                .HasColumnName("dt_processamento");

            builder.HasOne(pg => pg.Candidatura)
                .WithOne(c => c.PropostaGoverno)
                .HasForeignKey<PropostaGoverno>(pg => pg.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
