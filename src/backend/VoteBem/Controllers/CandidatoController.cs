using Microsoft.AspNetCore.Mvc;
using VoteBem.Services.Candidatos;

namespace VoteBem.Controllers
{
    [Route("candidatos")]
    [ApiController]
    public class CandidatoController(ICandidatoService candidatoService) : ControllerBase
    {
        [HttpGet("all-paginated")]
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

        [HttpGet("by-name-paginated")]
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

        [HttpGet("by-partido-paginated")]
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


        [HttpGet("by-ano-eleitoral-paginated")]
        public async Task<IActionResult> GetCandidatosByAnoEleitoralPaginated(int ano, int pageNumber = 1, int pageSize = 10)
        {
            try
            {
                var candidatosPaginated = await candidatoService.GetCandidatosByAnoEleitoralPaginatedAsync(pageNumber, pageSize, ano);
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

        [HttpGet("profile")]
        public async Task<IActionResult> GetCandidatoProfileAsync(string nrCpfCandidato)
        {
            try
            {
                var candidatoProfile = await candidatoService.GetCandidatoProfileAsync(nrCpfCandidato);
                return Ok(candidatoProfile);
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
