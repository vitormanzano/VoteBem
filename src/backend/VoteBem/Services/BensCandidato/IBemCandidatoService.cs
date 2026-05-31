using VoteBem.Dtos.BensCandidato;

namespace VoteBem.Services.BensCandidato
{
    public interface IBemCandidatoService
    {
        Task<IEnumerable<BemCandidatoResponseDto>> GetBensCandidatoBySqCandidatoAsync(long sqCandidato);
    }
}
