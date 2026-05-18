using NSubstitute;
using VoteBem.Entities;
using VoteBem.Repository.BensCadidato;
using VoteBem.Services.BensCandidato;

namespace VoteBemTest;

public class BemCandidatoServiceTests
{
    private readonly IBemCandidatoRepository _repository;
    private readonly BemCandidatoService _service;

    public BemCandidatoServiceTests()
    {
        _repository = Substitute.For<IBemCandidatoRepository>();
        _service = new BemCandidatoService(_repository);
    }

    [Fact]
    public async Task GetBensCandidatoBySqCandidatoAsync_SqValido_DeveRetornarLista()
    {
        _repository
            .GetBensCandidatoBySqCandidatoAsync(123L)
            .Returns(new List<BemCandidato>());

        var result = await _service.GetBensCandidatoBySqCandidatoAsync(123L);

        Assert.NotNull(result);
    }

    [Fact]
    public async Task GetBensCandidatoBySqCandidatoAsync_SqValido_DeveConsultarRepositorio()
    {
        _repository
            .GetBensCandidatoBySqCandidatoAsync(Arg.Any<long>())
            .Returns(new List<BemCandidato>());

        await _service.GetBensCandidatoBySqCandidatoAsync(456L);

        await _repository.Received(1).GetBensCandidatoBySqCandidatoAsync(456L);
    }
}
