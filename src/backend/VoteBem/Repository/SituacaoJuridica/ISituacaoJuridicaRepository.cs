using VoteBem.Data.UnitOfWork;
using VoteBem.Entities;

namespace VoteBem.Repository.SituacaoJuridica
{
    public interface ISituacaoJuridicaRepository
    {
        IUnitOfWork UnitOfWork { get; }

        Task<IEnumerable<CertidaoCriminal>> GetCertidoesCriminaisBySqCandidatoAsync(long sqCandidato);
        Task<IEnumerable<MotivoCassacao>> GetMotivosCassacaoBySqCandidatoAsync(long sqCandidato);
    }
}
