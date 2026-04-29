using VoteBem.Dtos.SituacaoJuridica;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class SituacaoJuridicaMapper
    {
        public static CertidaoCriminalResponseDto MapToCertidaoCriminalResponseDto(this CertidaoCriminal certidao)
        {
            return new CertidaoCriminalResponseDto
            (
                certidao.SqCandidato,
                certidao.NmArquivo,
                certidao.DsCaminhoArquivo
            );
        }

        public static MotivoCassacaoResponseDto MapToMotivoCassacaoResponseDto(this MotivoCassacao motivo)
        {
            return new MotivoCassacaoResponseDto
            (
                motivo.SqCandidato,
                motivo.DsTpMotivo,
                motivo.DsMotivo
            );
        }
    }
}
