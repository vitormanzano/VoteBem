using Microsoft.AspNetCore.Http.HttpResults;
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
                    _ => StatusCode(StatusCodes.Status500InternalServerError, ex.Message)
                };
            }
        }

        [HttpGet("GetCandidatosByNamePaginated")]
        public async Task<IActionResult> GetCandidatosByNamePaginated(string name, int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var candidatosPaginated = await candidatoService.GetCandidatosByNamePaginatedAsync(pageNumber, pageSize, name);
                return Ok(candidatosPaginated);

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

        [HttpGet("GetCandidatosByPartidoPaginated")]
        public async Task<IActionResult> GetCandidatosByPartidoPaginated(string partido, int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var candidatosPaginated = await candidatoService.GetCandidatosByPartidoPaginatedAsync(pageNumber, pageSize, partido);
                return Ok(candidatosPaginated);

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
