using Microsoft.EntityFrameworkCore;
using VoteBem.Data.Configurations;
using VoteBem.Entities;
using VoteBem.Data.UnitOfWork;

namespace VoteBem.Data
{
    public class AppDbContext : DbContext, IUnitOfWork
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

        public DbSet<Eleicao> Eleicoes { get; set; }
        public DbSet<Partido> Partidos { get; set; }
        public DbSet<Candidato> Candidatos { get; set; }
        public DbSet<Coligacao> Coligacoes { get; set; }
        public DbSet<Candidatura> Candidaturas { get; set; }
        public DbSet<ResultadoTurno> ResultadosTurno { get; set; }
        public DbSet<BemCandidato> BensCandidato { get; set; }
        public DbSet<RedeSocial> RedesSociais { get; set; }
        public DbSet<PropostaGoverno> PropostasGoverno { get; set; }
        public DbSet<ResumoProposta> ResumosProposta { get; set; }
        public DbSet<CertidaoCriminal> CertidoesCriminais { get; set; }
        public DbSet<MotivoCassacao> MotivosCassacao { get; set; }
        public DbSet<DespesaCandidato> DespesasCandidato { get; set; }
        public DbSet<NotaFiscal> NotasFiscais { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.ApplyConfiguration(new EleicaoConfiguration());
            modelBuilder.ApplyConfiguration(new PartidoConfiguration());
            modelBuilder.ApplyConfiguration(new CandidatoConfiguration());
            modelBuilder.ApplyConfiguration(new ColigacaoConfiguration());
            modelBuilder.ApplyConfiguration(new CandidaturaConfiguration());
            modelBuilder.ApplyConfiguration(new ResultadoTurnoConfiguration());
            modelBuilder.ApplyConfiguration(new BemCandidatoConfiguration());
            modelBuilder.ApplyConfiguration(new RedeSocialConfiguration());
            modelBuilder.ApplyConfiguration(new PropostaGovernoConfiguration());
            modelBuilder.ApplyConfiguration(new ResumoPropostaConfiguration());
            modelBuilder.ApplyConfiguration(new CertidaoCriminalConfiguration());
            modelBuilder.ApplyConfiguration(new MotivoCassacaoConfiguration());
            modelBuilder.ApplyConfiguration(new DespesaCandidatoConfiguration());
            modelBuilder.ApplyConfiguration(new NotaFiscalConfiguration());
        }

        public async Task<bool> CommitAsync()
        {           
            foreach (var entry in ChangeTracker.Entries().Where(entry => entry.State.GetType().GetProperty("CreatedAt") != null))
            {
                if (entry.State == EntityState.Added)
                {
                    entry.Property("CreatedAt").CurrentValue = DateTime.UtcNow;
                }
                else if (entry.State == EntityState.Modified)
                {
                    entry.Property("UpdatedAt").CurrentValue = DateTime.UtcNow;
                }
            }

            return await base.SaveChangesAsync() > 0;
        }
    }
}
    
}
