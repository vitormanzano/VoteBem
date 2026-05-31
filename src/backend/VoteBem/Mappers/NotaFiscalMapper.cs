using System.Globalization;
using VoteBem.Dtos.NotasFiscais;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class NotaFiscalMapper
    {
        public static NotaFiscalResponseDto MapToNotaFiscalResponseDto(this NotaFiscal notaFiscal)
        {
            return new NotaFiscalResponseDto
            (
                notaFiscal.NrNotaFiscal,
                notaFiscal.CpfCnpjEmitente,
                notaFiscal.DtEmissao?.ToString("dd/MM/yyyy"),
                notaFiscal.VrNotaFiscal.HasValue ? $"R${notaFiscal.VrNotaFiscal.Value.ToString("N2", CultureInfo.GetCultureInfo("pt-BR"))}" : null,
                notaFiscal.NmUrlAcesso
            );
        }
    }
}
