using VoteBem.Dtos.Ai;

namespace VoteBem.Services.IA
{
    public interface IAiService
    {
        Task<ChatResponseDto> ChatAsync(ChatRequestDto request, CancellationToken ct = default);
        Task<CompararResponseDto> CompararPropostasAsync(CompararRequestDto request, CancellationToken ct = default);
        Task<IEnumerable<ResumoPropostaDto>> GetResumosBySqCandidatoAsync(long sqCandidato);
    }
}
