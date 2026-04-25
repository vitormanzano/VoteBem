using Microsoft.AspNetCore.Mvc;
using VoteBem.Services.BensCandidato;
using VoteBem.Services.Candidatos;

namespace VoteBem.Controllers
{
    [Route("bem-candidatos")]
    [ApiController]
    public class BemCandidatoController(IBemCandidatoService bemCandidatoService) : ControllerBase
    {
        [HttpGet("all-by-candidato")]
        public async Task<IActionResult> GetAllByCandidato(long sqCandidato)
        {
            try
            {
                var bens = await bemCandidatoService.GetBensCandidatoBySqCandidatoAsync(sqCandidato);
                return Ok(bens);
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
