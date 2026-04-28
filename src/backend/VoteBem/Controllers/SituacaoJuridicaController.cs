using Microsoft.AspNetCore.Mvc;
using VoteBem.Services.SituacaoJuridica;

namespace VoteBem.Controllers
{
    [Route("situacao-juridica")]
    [ApiController]
    public class SituacaoJuridicaController(ISituacaoJuridicaService situacaoJuridicaService) : ControllerBase
    {
        [HttpGet("all-by-Sqcandidato")]
        public async Task<IActionResult> GetAllBySqCandidato(long sqCandidato)
        {
            try
            {
                var situacaoJuridica = await situacaoJuridicaService.GetSituacaoJuridicaBySqCandidatoAsync(sqCandidato);
                return Ok(situacaoJuridica);
            }
            catch (Exception ex)
            {
                return ex switch
                {
                    _ => StatusCode(StatusCodes.Status500InternalServerError, ex.Message)
                };
            }
        }
    }
}
