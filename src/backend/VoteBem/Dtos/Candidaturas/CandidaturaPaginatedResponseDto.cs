namespace VoteBem.Dtos.Candidaturas
{
    public record CandidaturaPaginatedResponseDto
        (
            string NomeUrna,
            string Partido,
            string CargoDisputado
        );
}
