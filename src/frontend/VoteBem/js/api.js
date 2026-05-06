/* ============================================================
   VOTO CONSCIENTE — api.js
   Camada de serviço: todas as chamadas ao backend .NET
   ============================================================ */

const API_BASE = 'http://localhost:5253';   // ← ajuste para o endereço do backend

// ── Utilitário ──────────────────────────────────────────────
async function apiFetch(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    const msg = await res.text().catch(() => res.statusText);
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return res.json();
}

// ============================================================
// CANDIDATOS
// ============================================================

/**
 * Lista paginada de todos os candidatos.
 * GET /candidatos/all-paginated
 * @returns PagedResultDto<CandidatoPaginatedResponseDto>
 */
export async function getCandidatosPaginated(pageNumber = 1, pageSize = 10) {
  return apiFetch(`/candidatos/all-paginated?pageNumber=${pageNumber}&pageSize=${pageSize}`);
}

/**
 * Lista paginada filtrada por nome de urna.
 * GET /candidatos/by-name-paginated
 * @returns PagedResultDto<CandidatoPaginatedResponseDto>
 */
export async function getCandidatosByName(name, pageNumber = 1, pageSize = 10) {
  return apiFetch(
    `/candidatos/by-name-paginated?name=${encodeURIComponent(name)}&pageNumber=${pageNumber}&pageSize=${pageSize}`
  );
}

/**
 * Lista paginada filtrada por sigla do partido.
 * GET /candidatos/by-partido-paginated
 * @returns PagedResultDto<CandidatoPaginatedResponseDto>
 */
export async function getCandidatosByPartido(partido, pageNumber = 1, pageSize = 10) {
  return apiFetch(
    `/candidatos/by-partido-paginated?partido=${encodeURIComponent(partido)}&pageNumber=${pageNumber}&pageSize=${pageSize}`
  );
}

/**
 * Lista paginada filtrada por ano eleitoral.
 * GET /candidatos/by-ano-eleitoral-paginated
 * @returns PagedResultDto<CandidatoPaginatedResponseDto>
 */
export async function getCandidatosByAno(ano, pageNumber = 1, pageSize = 10) {
  return apiFetch(
    `/candidatos/by-ano-eleitoral-paginated?ano=${ano}&pageNumber=${pageNumber}&pageSize=${pageSize}`
  );
}

/**
 * Perfil completo de um candidato.
 * GET /candidatos/profile?nrCpfCandidato=...
 * @returns CandidatoProfileDto
 */
export async function getCandidatoProfile(nrCpfCandidato) {
  return apiFetch(`/candidatos/profile?nrCpfCandidato=${encodeURIComponent(nrCpfCandidato)}`);
}

// ============================================================
// BENS DO CANDIDATO
// ============================================================

/**
 * Lista de bens declarados por sqCandidato.
 * GET /bem-candidatos/all-by-candidatura?sqCandidato=...
 * @returns BemCandidatoResponseDto[]
 */
export async function getBensBySqCandidato(sqCandidato) {
  return apiFetch(`/bem-candidatos/all-by-candidatura?sqCandidato=${sqCandidato}`);
}

// ============================================================
// CANDIDATURAS
// ============================================================

/**
 * Histórico de candidaturas (paginado) por CPF.
 * GET /candidaturas/all-by-candidato-paginated
 * @returns PagedResultDto<CandidaturaResponseDto>
 */
export async function getCandidaturasByCpf(nrCpfCandidato, pageNumber = 1, pageSize = 10) {
  return apiFetch(
    `/candidaturas/all-by-candidato-paginated?nrCpfCandidato=${encodeURIComponent(nrCpfCandidato)}&pageNumber=${pageNumber}&pageSize=${pageSize}`
  );
}

// ============================================================
// NOTAS FISCAIS
// ============================================================

/**
 * Notas fiscais de campanha (paginado) por sqCandidato.
 * GET /nota-fiscal/all-by-candidatura
 * @returns PagedResultDto<NotaFiscalResponseDto>
 */
export async function getNotasFiscaisBySqCandidato(sqCandidato, pageNumber = 1, pageSize = 10) {
  return apiFetch(
    `/nota-fiscal/all-by-candidatura?sqCandidato=${sqCandidato}&pageNumber=${pageNumber}&pageSize=${pageSize}`
  );
}

// ============================================================
// REDES SOCIAIS
// ============================================================

/**
 * Redes sociais (paginado) por sqCandidato.
 * GET /rede-social/all-by-candidatura
 * @returns PagedResultDto<RedeSocialResponseDto>
 */
export async function getRedesSociaisBySqCandidato(sqCandidato, pageNumber = 1, pageSize = 10) {
  return apiFetch(
    `/rede-social/all-by-candidatura?sqCandidato=${sqCandidato}&pageNumber=${pageNumber}&pageSize=${pageSize}`
  );
}

// ============================================================
// SITUAÇÃO JURÍDICA
// ============================================================

/**
 * Situação jurídica por sqCandidato.
 * GET /situacao-juridica/all-by-candidatura
 * @returns SituacaoJuridicaResponseDto { certidoesCriminais, motivosCassacao }
 */
export async function getSituacaoJuridicaBySqCandidato(sqCandidato) {
  return apiFetch(`/situacao-juridica/all-by-candidatura?sqCandidato=${sqCandidato}`);
}