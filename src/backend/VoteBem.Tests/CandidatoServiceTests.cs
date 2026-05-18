using NSubstitute;
using NSubstitute.ReturnsExtensions;
using VoteBem.Entities;
using VoteBem.Repository.Candidatos;
using VoteBem.Services.Candidatos;

namespace VoteBemTest;

public class CandidatoServiceTests
{
    private readonly ICandidatoRepository _repository;
    private readonly CandidatoService _service;

    public CandidatoServiceTests()
    {
        _repository = Substitute.For<ICandidatoRepository>();
        _service = new CandidatoService(_repository);
    }

    // GetCandidatoProfileAsync

    [Fact]
    public async Task GetCandidatoProfileAsync_CpfVazio_DeveLancarArgumentException()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetCandidatoProfileAsync("   "));
    }

    [Fact]
    public async Task GetCandidatoProfileAsync_CpfNaoEncontrado_DeveLancarArgumentException()
    {
        _repository.GetCandidatoByNrCpfAsync(Arg.Any<string>()).ReturnsNull();

        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetCandidatoProfileAsync("00000000000"));
    }

    // GetCandidatosByNamePaginatedAsync

    [Fact]
    public async Task GetCandidatosByNamePaginatedAsync_NomeVazio_DeveLancarArgumentException()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetCandidatosByNamePaginatedAsync(1, 10, ""));
    }

    [Fact]
    public async Task GetCandidatosByNamePaginatedAsync_NomeValido_DeveRetornarPaginado()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetCandidatosByNamePaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((candidatos.AsEnumerable(), 0));

        var result = await _service.GetCandidatosByNamePaginatedAsync(1, 10, "lula");

        Assert.NotNull(result);
        Assert.Equal(1, result.Page);
        Assert.Equal(10, result.PageSize);
    }

    [Fact]
    public async Task GetCandidatosByNamePaginatedAsync_NomeComEspacos_DeveAparar()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetCandidatosByNamePaginatedAsync(Arg.Any<int>(), Arg.Any<int>(), Arg.Any<string>())
            .Returns((candidatos.AsEnumerable(), 0));

        // Não deve lançar exceção mesmo com espaços nas bordas
        var result = await _service.GetCandidatosByNamePaginatedAsync(1, 10, "  lula  ");

        Assert.NotNull(result);

        await _repository.Received(1)
        .GetCandidatosByNamePaginatedAsync(1, 10, "lula");
    }

    // GetCandidatosByPartidoPaginatedAsync

    [Fact]
    public async Task GetCandidatosByPartidoPaginatedAsync_PartidoVazio_DeveLancarArgumentException()
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetCandidatosByPartidoPaginatedAsync(1, 10, ""));
    }

    [Fact]
    public async Task GetCandidatosByPartidoPaginatedAsync_PartidoValido_DeveRetornarPaginado()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetCandidatosByPartidoPaginatedAsync(1, 10, "PT")
            .Returns((candidatos.AsEnumerable(), 0));

        var result = await _service.GetCandidatosByPartidoPaginatedAsync(1, 10, "pt");

        Assert.NotNull(result);
        Assert.Equal(1, result.Page);
    }

    [Fact]
    public async Task GetCandidatosByPartidoPaginatedAsync_PartidoMinusculo_DeveConverterParaMaiusculo()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetCandidatosByPartidoPaginatedAsync(1, 10, "PT")
            .Returns((candidatos.AsEnumerable(), 0));

        // Deve passar "PT" ao repositório, não "pt"
        await _service.GetCandidatosByPartidoPaginatedAsync(1, 10, "pt");

        await _repository.Received(1)
            .GetCandidatosByPartidoPaginatedAsync(1, 10, "PT");
    }

    // GetCandidatosByAnoEleitoralPaginatedAsync

    [Theory]
    [InlineData(2010)]
    [InlineData(2014)]
    [InlineData(2018)]
    [InlineData(2022)]
    public async Task GetCandidatosByAnoEleitoralPaginatedAsync_AnoValido_DeveRetornarPaginado(int ano)
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetCandidatosByAnoEleitoralPaginatedAsync(1, 10, ano)
            .Returns((candidatos.AsEnumerable(), 0));

        var result = await _service.GetCandidatosByAnoEleitoralPaginatedAsync(1, 10, ano);

        Assert.NotNull(result);
        Assert.Equal(1, result.Page);
    }

    [Theory]
    [InlineData(2000)]
    [InlineData(2023)]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetCandidatosByAnoEleitoralPaginatedAsync_AnoInvalido_DeveLancarArgumentException(int ano)
    {
        await Assert.ThrowsAsync<ArgumentException>(() =>
            _service.GetCandidatosByAnoEleitoralPaginatedAsync(1, 10, ano));
    }
    
    // GetAllCandidatosPaginatedAsync — paginação

    [Fact]
    public async Task GetAllCandidatosPaginatedAsync_DeveCalcularTotalPaginasCorretamente()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetAllCandidatosPaginatedAsync(1, 10)
            .Returns((candidatos.AsEnumerable(), 25)); // 25 itens → 3 páginas

        var result = await _service.GetAllCandidatosPaginatedAsync(1, 10);

        Assert.Equal(3, result.TotalPages);
        Assert.Equal(25, result.TotalItems);
    }

    [Fact]
    public async Task GetAllCandidatosPaginatedAsync_PrimeiraPagina_NaoDeveTerPaginaAnterior()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetAllCandidatosPaginatedAsync(1, 10)
            .Returns((candidatos.AsEnumerable(), 30));

        var result = await _service.GetAllCandidatosPaginatedAsync(1, 10);

        Assert.False(result.HasPreviousPage);
        Assert.True(result.HasNextPage);
    }

    [Fact]
    public async Task GetAllCandidatosPaginatedAsync_UltimaPagina_NaoDeveTerProximaPagina()
    {
        var candidatos = new List<Candidato>();
        _repository
            .GetAllCandidatosPaginatedAsync(3, 10)
            .Returns((candidatos.AsEnumerable(), 30));

        var result = await _service.GetAllCandidatosPaginatedAsync(3, 10);

        Assert.True(result.HasPreviousPage);
        Assert.False(result.HasNextPage);
    }
}
