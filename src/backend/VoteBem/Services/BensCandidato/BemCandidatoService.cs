using VoteBem.Dtos.BensCandidato;
using VoteBem.Mappers;
using VoteBem.Repository.BensCadidato;

namespace VoteBem.Services.BensCandidato
{
    public class BemCandidatoService(IBemCandidatoRepository bemCandidatoRepository) : IBemCandidatoService
    {
        public async Task<IEnumerable<BemCandidatoResponseDto>> GetBensCandidatoBySqCandidatoAsync(long sqCandidato)
        {
            if (sqCandidato == null)
                throw new Exception("sqCandidato é obrigatório!");

            var bensCandidato = await bemCandidatoRepository.GetBensCandidatoBySqCandidatoAsync(sqCandidato);

            return bensCandidato.Select(bc => bc.MapToBemCandidatoResponseDto());
        }
    }
}
