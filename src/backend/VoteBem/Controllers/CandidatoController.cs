using Microsoft.AspNetCore.Mvc;
using VoteBem.Services.Candidatos;

namespace VoteBem.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class CandidatoController(ICandidatoService candidatoService) : ControllerBase
    {
        [HttpGet("GetAllCandidatosPaginated")]
        public async Task<IActionResult> GetAllCandidatosPaginated(int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var candidatosPaginated = await candidatoService.GetAllCandidatosPaginatedAsync(pageNumber, pageSize);
                return Ok(candidatosPaginated);
            }
            catch (Exception ex)
            {
                return ex switch
                {
                    _ => BadRequest(ex.Message)
                };
            }
        }
    }
}
