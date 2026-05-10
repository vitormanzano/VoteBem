using Microsoft.AspNetCore.Mvc;
using VoteBem.Dtos.Ai;
using VoteBem.Services.IA;

namespace VoteBem.Controllers
{
    [ApiController]
    [Route("ai")]
    public class AiController(IAiService aiService) : ControllerBase
    {
        [HttpGet("propostas/{sqCandidato:long}")]
        public async Task<IActionResult> GetPropostaGoverno(long sqCandidato)
        {
            try
            {
                var proposta = await aiService.GetPropostaGovernoAsync(sqCandidato);
                if (proposta is null) return NotFound();
                return Ok(proposta);
            }
            catch (Exception ex)
            {
                return ex switch
                {
                    ArgumentException => BadRequest(ex.Message),
                    _ => StatusCode(StatusCodes.Status500InternalServerError, ex.Message)
                };
            }
        }

        [HttpGet("propostas/{sqCandidato:long}/resumos")]
        public async Task<IActionResult> GetPropostasResumos(long sqCandidato)
        {
            try
            {
                var resumos = await aiService.GetResumosBySqCandidatoAsync(sqCandidato);
                return Ok(resumos);
            }
            catch (Exception ex)
            {
                return ex switch
                {
                    ArgumentException => BadRequest(ex.Message),
                    _ => StatusCode(StatusCodes.Status500InternalServerError, ex.Message)
                };
            }
        }

        [HttpPost("chat")]
        public async Task<IActionResult> ChatPrompt([FromBody] ChatRequestDto request, CancellationToken ct)
        {
            try
            {
                if (request is null || string.IsNullOrWhiteSpace(request.Pergunta))
                    return BadRequest("Pergunta é obrigatória.");

                var resposta = await aiService.ChatAsync(request, ct);
                return Ok(resposta);
            }
            catch (Exception ex)
            {
                return ex switch
                {
                    ArgumentException => BadRequest(ex.Message),
                    HttpRequestException httpEx => StatusCode(StatusCodes.Status502BadGateway, httpEx.Message),
                    _ => StatusCode(StatusCodes.Status500InternalServerError, ex.Message)
                };
            }
        }

        [HttpPost("propostas/comparar")]
        public async Task<IActionResult> CompararPropostas([FromBody] CompararRequestDto request, CancellationToken ct)
        {
            try
            {
                if (request is null)
                    return BadRequest("Body é obrigatório.");

                var resposta = await aiService.CompararPropostasAsync(request, ct);
                return Ok(resposta);
            }
            catch (Exception ex)
            {
                return ex switch
                {
                    ArgumentException => BadRequest(ex.Message),
                    HttpRequestException httpEx => StatusCode(StatusCodes.Status502BadGateway, httpEx.Message),
                    _ => StatusCode(StatusCodes.Status500InternalServerError, ex.Message)
                };
            }
        }
    }
}
