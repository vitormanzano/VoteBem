using NSubstitute;
using VoteBem.Entities;
using VoteBem.Repository.RedesSociais;
using VoteBem.Services.RedesSociais;

namespace VoteBemTest;

public class RedeSocialServiceTests
{
    private readonly IRedeSocialRepository _repository;
    private readonly RedeSocialService _service;

    public RedeSocialServiceTests()
    {
        _repository = Substitute.For<IRedeSocialRepository>();
        _service = new RedeSocialService(_repository);
    }

    [Fact]
    public async Task GetAllBySqCandidatoPaginatedAsync_SqValido_DeveRetornarPaginado()
    {
        _repository
            .GetRedesSociaisBySqCandidatoPaginatedAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<RedeSocial>().AsEnumerable(), 0));

        var result = await _service.GetAllBySqCandidatoPaginatedAsync(123L, 1, 10);

        Assert.NotNull(result);
        Assert.Equal(1, result.Page);
        Assert.Equal(10, result.PageSize);
    }

    [Fact]
    public async Task GetAllBySqCandidatoPaginatedAsync_DeveCalcularTotalPaginasCorretamente()
    {
        _repository
            .GetRedesSociaisBySqCandidatoPaginatedAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<RedeSocial>().AsEnumerable(), 25));

        var result = await _service.GetAllBySqCandidatoPaginatedAsync(123L, 1, 10);

        Assert.Equal(3, result.TotalPages);
        Assert.Equal(25, result.TotalItems);
    }

    [Fact]
    public async Task GetAllBySqCandidatoPaginatedAsync_PrimeiraPagina_NaoDeveTerPaginaAnterior()
    {
        _repository
            .GetRedesSociaisBySqCandidatoPaginatedAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<RedeSocial>().AsEnumerable(), 30));

        var result = await _service.GetAllBySqCandidatoPaginatedAsync(123L, 1, 10);

        Assert.False(result.HasPreviousPage);
        Assert.True(result.HasNextPage);
    }

    [Fact]
    public async Task GetAllBySqCandidatoPaginatedAsync_UltimaPagina_NaoDeveTerProximaPagina()
    {
        _repository
            .GetRedesSociaisBySqCandidatoPaginatedAsync(Arg.Any<long>(), Arg.Any<int>(), Arg.Any<int>())
            .Returns((new List<RedeSocial>().AsEnumerable(), 30));

        var result = await _service.GetAllBySqCandidatoPaginatedAsync(123L, 3, 10);

        Assert.True(result.HasPreviousPage);
        Assert.False(result.HasNextPage);
    }
}
