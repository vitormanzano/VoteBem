using Microsoft.AspNetCore.Mvc;
using VoteBem.Services.NotasFiscais;

namespace VoteBem.Controllers
{
    [Route("nota-fiscal")]
    [ApiController]
    public class NotaFiscalController(INotaFiscalService notaFiscalService) : ControllerBase
    {
        [HttpGet("all-by-candidatura")]
        public async Task<IActionResult> GetAllByCandidato(long sqCandidato, int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var notasFiscais = await notaFiscalService.GetNotasFiscaisBySqCandidatoAsync(sqCandidato, pageNumber, pageSize);
                return Ok(notasFiscais);
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
