namespace VoteBem.Dtos.Candidatos
{
    public record CandidatoPaginatedResponseDto
         (
             string NomeUrna,
             string Partido,
             string CargoDisputado
         );
}
