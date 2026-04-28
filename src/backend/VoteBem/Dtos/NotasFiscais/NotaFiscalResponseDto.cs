namespace VoteBem.Dtos.NotasFiscais
{
    public record NotaFiscalResponseDto
        (
            string? NrNotaFiscal,
            string? CpfCnpjEmitente,
            string? DtEmissao,
            string? VrNotaFiscal,
            string? NmUrlAcesso
        );
}
