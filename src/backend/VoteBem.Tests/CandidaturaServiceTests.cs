using NSubstitute;
using VoteBem.Entities;
using VoteBem.Repository.Candidaturas;
using VoteBem.Services.Candidaturas;

namespace VoteBemTest;

public class CandidaturaServiceTests
{
    private readonly ICandidaturaRepository _repository;
    private readonly CandidaturaService _service;

    public CandidaturaServiceTests()
    {
        _repository = Substitute.For<ICandidaturaRepository>();
        _service = new CandidaturaService(_repository);
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_CpfVazio_DeveLancarArgumentException()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetAllByCandidatoPaginatedAsync(1, 10, ""));
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_CpfNulo_DeveLancarArgumentException()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetAllByCandidatoPaginatedAsync(1, 10, null!));
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_CpfValido_DeveRetornarPaginado()
    {
        _repository
            .GetAllByCandidatoPaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((new List<Candidatura>().AsEnumerable(), 0));
        _repository
            .GetAnosEleicaoAsync(Arg.Any<IEnumerable<long>>())
            .Returns(new Dictionary<long, int>());

        var result = await _service.GetAllByCandidatoPaginatedAsync(1, 10, "12345678900");

        Assert.NotNull(result);
        Assert.Equal(1, result.Page);
        Assert.Equal(10, result.PageSize);
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_CpfComEspacos_DeveAparar()
    {
        _repository
            .GetAllByCandidatoPaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((new List<Candidatura>().AsEnumerable(), 0));
        _repository
            .GetAnosEleicaoAsync(Arg.Any<IEnumerable<long>>())
            .Returns(new Dictionary<long, int>());

        await _service.GetAllByCandidatoPaginatedAsync(1, 10, "  12345678900  ");

        await _repository.Received(1)
            .GetAllByCandidatoPaginatedAsync(1, 10, "12345678900");
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_DeveCalcularTotalPaginasCorretamente()
    {
        _repository
            .GetAllByCandidatoPaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((new List<Candidatura>().AsEnumerable(), 25));
        _repository
            .GetAnosEleicaoAsync(Arg.Any<IEnumerable<long>>())
            .Returns(new Dictionary<long, int>());

        var result = await _service.GetAllByCandidatoPaginatedAsync(1, 10, "12345678900");

        Assert.Equal(0, result.TotalPages);
        Assert.Equal(0, result.TotalItems);
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_PrimeiraPagina_NaoDeveTerPaginaAnterior()
    {
        _repository
            .GetAllByCandidatoPaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((new List<Candidatura>().AsEnumerable(), 30));
        _repository
            .GetAnosEleicaoAsync(Arg.Any<IEnumerable<long>>())
            .Returns(new Dictionary<long, int>());

        var result = await _service.GetAllByCandidatoPaginatedAsync(1, 10, "12345678900");

        Assert.False(result.HasPreviousPage);
        Assert.False(result.HasNextPage);
    }

    [Fact]
    public async Task GetAllByCandidatoPaginatedAsync_UltimaPagina_NaoDeveTerProximaPagina()
    {
        _repository
            .GetAllByCandidatoPaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((new List<Candidatura>().AsEnumerable(), 30));
        _repository
            .GetAnosEleicaoAsync(Arg.Any<IEnumerable<long>>())
            .Returns(new Dictionary<long, int>());

        var result = await _service.GetAllByCandidatoPaginatedAsync(3, 10, "12345678900");

        Assert.True(result.HasPreviousPage);
        Assert.False(result.HasNextPage);
    }
}
