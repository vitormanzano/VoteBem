using VoteBem.Dtos.SituacaoJuridica;
using VoteBem.Mappers;
using VoteBem.Repository.SituacaoJuridica;

namespace VoteBem.Services.SituacaoJuridica
{
    public class SituacaoJuridicaService(ISituacaoJuridicaRepository situacaoJuridicaRepository) : ISituacaoJuridicaService
    {
        public async Task<SituacaoJuridicaResponseDto> GetSituacaoJuridicaBySqCandidatoAsync(long sqCandidato)
        {
            if (sqCandidato == null)
                throw new Exception("sqCandidato é obrigatório!");

            var certidoes = await situacaoJuridicaRepository.GetCertidoesCriminaisBySqCandidatoAsync(sqCandidato);
            var motivosCassacao = await situacaoJuridicaRepository.GetMotivosCassacaoBySqCandidatoAsync(sqCandidato);

            return new SituacaoJuridicaResponseDto(
                certidoes.Select(cc => cc.MapToCertidaoCriminalResponseDto()),
                motivosCassacao.Select(mc => mc.MapToMotivoCassacaoResponseDto())
            );
        }
    }
}
