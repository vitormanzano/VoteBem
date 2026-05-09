using System.Net.Http.Json;
using System.Text.Json;
using VoteBem.Dtos.Ai;
using VoteBem.Repository.ResumosProposta;

namespace VoteBem.Services.IA
{
    public class AiService(HttpClient httpClient, IResumoPropostaRepository resumoRepository) : IAiService
    {
        // Python responde em snake_case. Mapeamento JSON nas chamadas externas.
        private static readonly JsonSerializerOptions SnakeCaseJson = new()
        {
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
            PropertyNameCaseInsensitive = true,
        };

        public async Task<ChatResponseDto> ChatAsync(ChatRequestDto request, CancellationToken ct = default)
        {
            var resp = await httpClient.PostAsJsonAsync("ai/chat", request, SnakeCaseJson, ct);
            await EnsureSuccessOrThrowAsync(resp, ct);
            return await resp.Content.ReadFromJsonAsync<ChatResponseDto>(SnakeCaseJson, ct)
                   ?? throw new InvalidOperationException("Resposta vazia do serviço de IA.");
        }

        public async Task<CompararResponseDto> CompararPropostasAsync(CompararRequestDto request, CancellationToken ct = default)
        {
            if (request.SqCandidatos is null || !request.SqCandidatos.Any())
                throw new ArgumentException("É necessário informar ao menos 2 sq_candidatos para comparar.");
            if (request.SqCandidatos.Count() < 2 || request.SqCandidatos.Count() > 4)
                throw new ArgumentException("A comparação aceita entre 2 e 4 candidatos.");

            var resp = await httpClient.PostAsJsonAsync("ai/propostas/comparar", request, SnakeCaseJson, ct);
            await EnsureSuccessOrThrowAsync(resp, ct);
            return await resp.Content.ReadFromJsonAsync<CompararResponseDto>(SnakeCaseJson, ct)
                   ?? throw new InvalidOperationException("Resposta vazia do serviço de IA.");
        }

        public async Task<IEnumerable<ResumoPropostaDto>> GetResumosBySqCandidatoAsync(long sqCandidato)
        {
            if (sqCandidato <= 0)
                throw new ArgumentException("sq_candidato inválido.");

            var resumos = await resumoRepository.GetResumosBySqCandidatoAsync(sqCandidato);
            return resumos.Select(r => new ResumoPropostaDto
            {
                IdResumo = r.IdResumo,
                SqCandidato = r.SqCandidato,
                DsTema = r.DsTema,
                TxResumo = r.TxResumo,
                DtGeracao = r.DtGeracao,
            });
        }

        private static async Task EnsureSuccessOrThrowAsync(HttpResponseMessage resp, CancellationToken ct)
        {
            if (resp.IsSuccessStatusCode) return;

            var body = await resp.Content.ReadAsStringAsync(ct);
            throw new HttpRequestException(
                $"Falha ao chamar serviço de IA ({(int)resp.StatusCode} {resp.ReasonPhrase}): {body}",
                inner: null,
                statusCode: resp.StatusCode);
        }
    }
}
