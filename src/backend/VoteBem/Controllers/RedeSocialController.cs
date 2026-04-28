using Microsoft.AspNetCore.Mvc;
using System.Formats.Asn1;
using VoteBem.Services.RedesSociais;

namespace VoteBem.Controllers
{
    [Route("rede-social")]
    [ApiController]
    public class RedeSocialController(IRedeSocialService redeSocialService) : ControllerBase
    {
        [HttpGet("all-by-candidatura")]
        public async Task<IActionResult> GetAllBySqCandidatoPaginated(long sqCandidato, int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var redesSociais = await redeSocialService.GetAllBySqCandidatoPaginatedAsync(sqCandidato, pageNumber, pageSize);
                return Ok(redesSociais);
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
