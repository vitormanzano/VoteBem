using System.Net;
using System.Text;
using System.Text.Json;
using NSubstitute;
using VoteBem.Dtos.Ai;
using VoteBem.Entities;
using VoteBem.Repository.ResumosProposta;
using VoteBem.Services.IA;

namespace VoteBemTest;


// Fake handler para simular respostas HTTP sem chamar a rede de verdade

public class FakeHttpMessageHandler(HttpStatusCode statusCode, string responseBody) : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
    {
        var response = new HttpResponseMessage(statusCode)
        {
            Content = new StringContent(responseBody, Encoding.UTF8, "application/json")
        };
        return Task.FromResult(response);
    }
}

// AiServiceTests

public class AiServiceTests
{
    private readonly IResumoPropostaRepository _resumoRepository;

    public AiServiceTests()
    {
        _resumoRepository = Substitute.For<IResumoPropostaRepository>();
    }

    private AiService CriarServiceComRespostaHttp(HttpStatusCode statusCode, string body)
    {
        var handler = new FakeHttpMessageHandler(statusCode, body);
        var httpClient = new HttpClient(handler) { BaseAddress = new Uri("http://localhost:8001/") };
        return new AiService(httpClient, _resumoRepository);
    }

    // CompararPropostasAsync — validações de entrada (sem HTTP)

    [Fact]
    public async Task CompararPropostasAsync_ListaVazia_DeveLancarArgumentException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");
        var request = new CompararRequestDto { SqCandidatos = [] };

        await Assert.ThrowsAsync<ArgumentException>(() =>
            service.CompararPropostasAsync(request));
    }

    [Fact]
    public async Task CompararPropostasAsync_UmCandidato_DeveLancarArgumentException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");
        var request = new CompararRequestDto { SqCandidatos = [1L] };

        await Assert.ThrowsAsync<ArgumentException>(() =>
            service.CompararPropostasAsync(request));
    }

    [Fact]
    public async Task CompararPropostasAsync_CincoCandidatos_DeveLancarArgumentException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");
        var request = new CompararRequestDto { SqCandidatos = [1L, 2L, 3L, 4L, 5L] };

        await Assert.ThrowsAsync<ArgumentException>(() =>
            service.CompararPropostasAsync(request));
    }

    [Fact]
    public async Task CompararPropostasAsync_DoisCandidatos_DeveRetornarDto()
    {
        var responseBody = JsonSerializer.Serialize(new
        {
            candidatos = Array.Empty<object>(),
            comparacoes = Array.Empty<object>()
        });
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, responseBody);
        var request = new CompararRequestDto { SqCandidatos = [1L, 2L] };

        var result = await service.CompararPropostasAsync(request);

        Assert.NotNull(result);
    }

    [Fact]
    public async Task CompararPropostasAsync_QuatroCandidatos_DeveRetornarDto()
    {
        var responseBody = JsonSerializer.Serialize(new
        {
            candidatos = Array.Empty<object>(),
            comparacoes = Array.Empty<object>()
        });
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, responseBody);
        var request = new CompararRequestDto { SqCandidatos = [1L, 2L, 3L, 4L] };

        var result = await service.CompararPropostasAsync(request);

        Assert.NotNull(result);
    }

    [Fact]
    public async Task CompararPropostasAsync_RespostaErroHttp_DeveLancarHttpRequestException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.InternalServerError, "erro");
        var request = new CompararRequestDto { SqCandidatos = [1L, 2L] };

        await Assert.ThrowsAsync<HttpRequestException>(() =>
            service.CompararPropostasAsync(request));
    }

    // ChatAsync

    [Fact]
    public async Task ChatAsync_RespostaValida_DeveRetornarDto()
    {
        var responseBody = JsonSerializer.Serialize(new
        {
            resposta = "Resposta de teste",
            fontes = Array.Empty<object>(),
            categoria = "estruturada"
        });
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, responseBody);
        var request = new ChatRequestDto { Pergunta = "Qual o patrimônio de Lula?" };

        var result = await service.ChatAsync(request);

        Assert.NotNull(result);
    }

    [Fact]
    public async Task ChatAsync_RespostaErroHttp_DeveLancarHttpRequestException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.BadGateway, "erro");
        var request = new ChatRequestDto { Pergunta = "Pergunta qualquer" };

        await Assert.ThrowsAsync<HttpRequestException>(() =>
            service.ChatAsync(request));
    }

    // GetResumosBySqCandidatoAsync

    [Fact]
    public async Task GetResumosBySqCandidatoAsync_SqInvalido_DeveLancarArgumentException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");

        await Assert.ThrowsAsync<ArgumentException>(() =>
            service.GetResumosBySqCandidatoAsync(0L));
    }

    [Fact]
    public async Task GetResumosBySqCandidatoAsync_SqNegativo_DeveLancarArgumentException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");

        await Assert.ThrowsAsync<ArgumentException>(() =>
            service.GetResumosBySqCandidatoAsync(-1L));
    }

    [Fact]
    public async Task GetResumosBySqCandidatoAsync_SqValido_DeveRetornarResumos()
    {
        var resumos = new List<ResumoProposta>();
        _resumoRepository
            .GetResumosBySqCandidatoAsync(123L)
            .Returns(resumos);

        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");
        var result = await service.GetResumosBySqCandidatoAsync(123L);

        Assert.NotNull(result);
        await _resumoRepository.Received(1).GetResumosBySqCandidatoAsync(123L);
    }

    // GetPropostaGovernoAsync

    [Fact]
    public async Task GetPropostaGovernoAsync_SqInvalido_DeveLancarArgumentException()
    {
        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");

        await Assert.ThrowsAsync<ArgumentException>(() =>
            service.GetPropostaGovernoAsync(0L));
    }

    [Fact]
    public async Task GetPropostaGovernoAsync_PropostaNaoEncontrada_DeveRetornarNull()
    {
        _resumoRepository
            .GetPropostaGovernoAsync(999L)
            .Returns((PropostaGoverno?)null);

        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");
        var result = await service.GetPropostaGovernoAsync(999L);

        Assert.Null(result);
    }

    [Fact]
    public async Task GetPropostaGovernoAsync_PropostaEncontrada_DeveRetornarDto()
    {
        var proposta = (PropostaGoverno)Activator.CreateInstance(
        typeof(PropostaGoverno), nonPublic: true)!;

        typeof(PropostaGoverno)
        .GetProperty(nameof(PropostaGoverno.SqCandidato))!
        .SetValue(proposta, 123L);

        typeof(PropostaGoverno)
        .GetProperty(nameof(PropostaGoverno.NmArquivo))!
        .SetValue(proposta, "proposta.pdf");

        typeof(PropostaGoverno)
        .GetProperty(nameof(PropostaGoverno.StProcessado))!
        .SetValue(proposta, true);

        _resumoRepository
            .GetPropostaGovernoAsync(123L)
            .Returns(proposta);

        var service = CriarServiceComRespostaHttp(HttpStatusCode.OK, "{}");
        var result = await service.GetPropostaGovernoAsync(123L);

        Assert.NotNull(result);
        Assert.Equal(123L, result.SqCandidato);
        Assert.Equal("proposta.pdf", result.NmArquivo);
    }
}