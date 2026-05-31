/* ============================================================
   VOTO CONSCIENTE — api.js
   Camada de serviço: todas as chamadas ao backend .NET
   ============================================================ */

const API_BASE = 'http://localhost:5253';   // ← ajuste para o endereço do backend

// ── Utilitário ──────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const msg = await res.text().catch(() => res.statusText);
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return res.json();
}

async function apiPost(path, body) {
  return apiFetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
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

// ============================================================
// PROPOSTAS (IA)
// ============================================================

/**
 * Dados do PDF do programa de governo por sqCandidato.
 * GET /ai/propostas/{sqCandidato}
 * @returns PropostaGovernoDto | null (404 → null)
 */
export async function getPropostaGoverno(sqCandidato) {
  const res = await fetch(`${API_BASE}/ai/propostas/${sqCandidato}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * Resumos das propostas de governo gerados por IA por sqCandidato.
 * GET /ai/propostas/{sqCandidato}/resumos
 * @returns ResumoPropostaDto[]
 */
export async function getPropostasResumos(sqCandidato) {
  return apiFetch(`/ai/propostas/${sqCandidato}/resumos`);
}

// ============================================================
// IA — Chat, Comparação e Resumos de Propostas
// ============================================================

/**
 * Pergunta em linguagem natural para o chatbot.
 * POST /ai/chat
 * @param {string} pergunta
 * @returns ChatResponseDto { resposta, fontes, categoria }
 */
export async function chatIA(pergunta) {
  return apiPost('/ai/chat', { pergunta });
}

/**
 * Comparação de propostas de governo entre 2-4 candidatos.
 * POST /ai/propostas/comparar
 * @param {{ sqCandidatos: number[], temas?: string[] }} body
 * @returns CompararResponseDto { candidatos, comparacoes }
 */
export async function compararPropostasIA({ sqCandidatos, temas = null }) {
  const body = { sqCandidatos };
  if (temas && temas.length) body.temas = temas;
  return apiPost('/ai/propostas/comparar', body);
}

/**
 * Resumos pré-computados (por tema) das propostas de um candidato.
 * GET /ai/propostas/{sqCandidato}/resumos
 * @returns ResumoPropostaDto[] — { idResumo, sqCandidato, dsTema, txResumo, dtGeracao }
 */
export async function getResumosBySqCandidato(sqCandidato) {
  return apiFetch(`/ai/propostas/${sqCandidato}/resumos`);
}