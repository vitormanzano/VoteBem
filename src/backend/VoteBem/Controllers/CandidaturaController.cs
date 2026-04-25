using Microsoft.AspNetCore.Mvc;
using VoteBem.Services.Candidaturas;

namespace VoteBem.Controllers
{
    [Route("candidaturas")]
    [ApiController]
    public class CandidaturaController(ICandidaturaService candidaturaService) : ControllerBase
    {
        [HttpGet("all-by-candidato-paginated")]
        public async Task<IActionResult> GetAllByCandidatoPaginated(string nrCpfCandidato, int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var candidaturas = await candidaturaService.GetAllByCandidatoPaginatedAsync(pageNumber, pageSize, nrCpfCandidato);
                return Ok(candidaturas);
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
    }
}
