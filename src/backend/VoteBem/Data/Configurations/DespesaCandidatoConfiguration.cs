using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using VoteBem.Entities;

namespace VoteBem.Data.Configurations
{
    public class DespesaCandidatoConfiguration : IEntityTypeConfiguration<DespesaCandidato>
    {
        public void Configure(EntityTypeBuilder<DespesaCandidato> builder)
        {
            builder.ToTable("despesa_candidato");

            builder.HasKey(d => d.IdDespesa);

            builder.Property(d => d.IdDespesa)
                .HasColumnName("id_despesa")
                .UseIdentityAlwaysColumn();

            builder.Property(d => d.SqCandidato)
                .HasColumnName("sq_candidato")
                .IsRequired();

            builder.Property(d => d.NrDocumento)
                .HasColumnName("nr_documento");

            builder.Property(d => d.CpfCnpjFornecedor)
                .HasColumnName("cpf_cnpj_fornecedor");

            builder.Property(d => d.NmFornecedor)
                .HasColumnName("nm_fornecedor");

            builder.Property(d => d.DtDespesa)
                .HasColumnName("dt_despesa");

            builder.Property(d => d.VrDespesa)
                .HasColumnName("vr_despesa")
                .HasColumnType("DECIMAL(15,2)");

            builder.Property(d => d.DsTipoDespesa)
                .HasColumnName("ds_tipo_despesa");

            builder.Property(d => d.DsFonteRecurso)
                .HasColumnName("ds_fonte_recurso");

            builder.Property(d => d.DsEspecieRecurso)
                .HasColumnName("ds_especie_recurso");

            builder.Property(d => d.DsDespesa)
                .HasColumnName("ds_despesa");

            builder.HasIndex(d => new { d.SqCandidato, d.NrDocumento, d.CpfCnpjFornecedor, d.DtDespesa })
                .IsUnique();

            builder.HasOne(d => d.Candidatura)
                .WithMany(c => c.Despesas)
                .HasForeignKey(d => d.SqCandidato)
                .OnDelete(DeleteBehavior.Restrict);
        }
    }
}
