using VoteBem.Dtos.SituacaoJuridica;

namespace VoteBem.Services.SituacaoJuridica
{
    public interface ISituacaoJuridicaService
    {
        Task<SituacaoJuridicaResponseDto> GetSituacaoJuridicaBySqCandidatoAsync(long sqCandidato);
    }
}
