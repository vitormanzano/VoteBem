using NSubstitute;
using VoteBem.Entities;
using VoteBem.Repository.NotasFiscais;
using VoteBem.Services.NotasFiscais;

namespace VoteBemTest;

public class NotaFiscalServiceTests
{
    private readonly INotaFiscalRepository _repository;
    private readonly NotaFiscalService _service;

    public NotaFiscalServiceTests()
    {
        _repository = Substitute.For<INotaFiscalRepository>();
        _service = new NotaFiscalService(_repository);
    }

    [Fact]
    public async Task GetNotasFiscaisBySqCandidatoAsync_SqValido_DeveRetornarPaginado()
    {
        _repository
            .GetNotasFiscaisBySqCandidatoAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<NotaFiscal>().AsEnumerable(), 0));

        var result = await _service.GetNotasFiscaisBySqCandidatoAsync(123L, 1, 10);

        Assert.NotNull(result);
        Assert.Equal(1, result.Page);
        Assert.Equal(10, result.PageSize);
    }

    [Fact]
    public async Task GetNotasFiscaisBySqCandidatoAsync_DeveCalcularTotalPaginasCorretamente()
    {
        _repository
            .GetNotasFiscaisBySqCandidatoAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<NotaFiscal>().AsEnumerable(), 25));

        var result = await _service.GetNotasFiscaisBySqCandidatoAsync(123L, 1, 10);

        Assert.Equal(3, result.TotalPages);
        Assert.Equal(25, result.TotalItems);
    }

    [Fact]
    public async Task GetNotasFiscaisBySqCandidatoAsync_PrimeiraPagina_NaoDeveTerPaginaAnterior()
    {
        _repository
            .GetNotasFiscaisBySqCandidatoAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<NotaFiscal>().AsEnumerable(), 30));

        var result = await _service.GetNotasFiscaisBySqCandidatoAsync(123L, 1, 10);

        Assert.False(result.HasPreviousPage);
        Assert.True(result.HasNextPage);
    }

    [Fact]
    public async Task GetNotasFiscaisBySqCandidatoAsync_UltimaPagina_NaoDeveTerProximaPagina()
    {
        _repository
            .GetNotasFiscaisBySqCandidatoAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<NotaFiscal>().AsEnumerable(), 30));

        var result = await _service.GetNotasFiscaisBySqCandidatoAsync(123L, 3, 10);

        Assert.True(result.HasPreviousPage);
        Assert.False(result.HasNextPage);
    }
}
