using NSubstitute;
using VoteBem.Entities;
using VoteBem.Repository.SituacaoJuridica;
using VoteBem.Services.SituacaoJuridica;

namespace VoteBemTest;

public class SituacaoJuridicaServiceTests
{
    private readonly ISituacaoJuridicaRepository _repository;
    private readonly SituacaoJuridicaService _service;

    public SituacaoJuridicaServiceTests()
    {
        _repository = Substitute.For<ISituacaoJuridicaRepository>();
        _service = new SituacaoJuridicaService(_repository);
    }

    [Fact]
    public async Task GetSituacaoJuridicaBySqCandidatoAsync_SqValido_DeveRetornarDto()
    {
        _repository
            .GetCertidoesCriminaisBySqCandidatoAsync(Arg.Any<long>())
            .Returns(new List<CertidaoCriminal>());
        _repository
            .GetMotivosCassacaoBySqCandidatoAsync(Arg.Any<long>())
            .Returns(new List<MotivoCassacao>());

        var result = await _service.GetSituacaoJuridicaBySqCandidatoAsync(123L);

        Assert.NotNull(result);
    }

    [Fact]
    public async Task GetSituacaoJuridicaBySqCandidatoAsync_SqValido_DeveConsultarCertidoes()
    {
        _repository
            .GetCertidoesCriminaisBySqCandidatoAsync(Arg.Any<long>())
            .Returns(new List<CertidaoCriminal>());
        _repository
            .GetMotivosCassacaoBySqCandidatoAsync(Arg.Any<long>())
            .Returns(new List<MotivoCassacao>());

        await _service.GetSituacaoJuridicaBySqCandidatoAsync(123L);

        await _repository.Received(1).GetCertidoesCriminaisBySqCandidatoAsync(123L);
        await _repository.Received(1).GetMotivosCassacaoBySqCandidatoAsync(123L);
    }
}
