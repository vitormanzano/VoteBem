using VoteBem.Dtos.BensCandidato;
using VoteBem.Mappers;
using VoteBem.Repository.BensCadidato;

namespace VoteBem.Services.BensCandidato
{
    public class BemCandidatoService(IBemCandidatoRepository bemCandidatoRepository) : IBemCandidatoService
    {
        public async Task<IEnumerable<BemCandidatoResponseDto>> GetBensCandidatoBySqCandidatoAsync(long sqCandidato)
        {

            var bensCandidato = await bemCandidatoRepository.GetBensCandidatoBySqCandidatoAsync(sqCandidato);

            return bensCandidato.Select(bc => bc.MapToBemCandidatoResponseDto());
        }
    }
}
