using VoteBem.Dtos.RedesSociais;
using VoteBem.Entities;

namespace VoteBem.Mappers
{
    public static class RedeSocialMapper
    {
        public static RedeSocialResponseDto MapRedeSocialToRedeSocialResponseDto(this RedeSocial redeSocial)
        {
            return new RedeSocialResponseDto(
                redeSocial.TipoRedeSocial,
                redeSocial.DsUrl
                );
            
        }
    }
}
