using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class ColigacaoConfiguration : IEntityTypeConfiguration<Coligacao>
    {
        public void Configure(EntityTypeBuilder<Coligacao> builder)
        {
            builder.ToTable("coligacao");

            builder.HasKey(c => c.SqColigacao);

            builder.Property(c => c.SqColigacao)
                .HasColumnName("sq_coligacao")
                .IsRequired();

            builder.Property(c => c.CdEleicao)
                .HasColumnName("cd_eleicao")
                .IsRequired();

            builder.Property(c => c.NrTurno)
                .HasColumnName("nr_turno")
                .IsRequired();

            builder.Property(c => c.NmColigacao)
                .HasColumnName("nm_coligacao");

            builder.Property(c => c.DsComposicaoColigacao)
                .HasColumnName("ds_composicao_coligacao");

            builder.Property(c => c.TpAgremiacao)
                .HasColumnName("tp_agremiacao");

            builder.Property(c => c.SgUf)
                .HasColumnName("sg_uf")
                .HasMaxLength(2);

            builder.HasOne(c => c.Eleicao)
                .WithMany(e => e.Coligacoes)
                .HasForeignKey(c => new { c.CdEleicao, c.NrTurno});
        }
    }
}
