namespace VoteBem.Dtos.Candidatos
{
    public record CandidatoPaginatedResponseDto
         (
             string NrCpfCandidato,
             string NomeUrna,
             string Partido,
             string CargoDisputado
         );
}
