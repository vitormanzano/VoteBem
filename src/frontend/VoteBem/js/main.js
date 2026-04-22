/* ============================================================
   VOTO CONSCIENTE — main.js
   Módulos: NavDrawer · SearchBox · Suggestions · Candidates · ScrollReveal
   ============================================================ */

/* ── 1. NAV DRAWER (mobile toggle) ── */
const menuToggle = document.getElementById('menuToggle');
const navDrawer  = document.getElementById('navDrawer');

if (menuToggle && navDrawer) {
  menuToggle.addEventListener('click', () => {
    const isOpen = navDrawer.classList.toggle('is-open');
    menuToggle.setAttribute('aria-expanded', isOpen);
  });

  // Fecha ao clicar fora
  document.addEventListener('click', (e) => {
    if (!menuToggle.contains(e.target) && !navDrawer.contains(e.target)) {
      navDrawer.classList.remove('is-open');
      menuToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ── 2. SEARCH BOX ── */
const searchInput = document.getElementById('searchInput');
const submitBtn   = document.getElementById('submitBtn');

/**
 * Envia a pergunta do usuário.
 * Substituir pelo fetch/call real quando o backend estiver pronto.
 */
function handleSearch() {
  const query = searchInput?.value.trim();
  if (!query) return;

  console.log('[VotoConsciente] Pergunta enviada:', query);

  // TODO: chamar API / módulo de IA
  // exemplo: fetchAnswer(query).then(renderResponse);
}

submitBtn?.addEventListener('click', handleSearch);

searchInput?.addEventListener('keydown', (e) => {
  // Ctrl+Enter ou Cmd+Enter envia
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
    e.preventDefault();
    handleSearch();
  }
});

/* ── 3. SUGGESTION CHIPS ── */
const chips = document.querySelectorAll('.suggestions__chip');

chips.forEach((chip) => {
  chip.addEventListener('click', () => {
    if (searchInput) {
      searchInput.value = chip.textContent.trim();
      searchInput.focus();
    }
  });
});

/* ── 4. CANDIDATES (dados de exemplo) ── */
const CANDIDATES_DATA = [
  { name: 'Lula',      initials: 'LU', party: 'PT'    },
  { name: 'Bolsonaro', initials: 'JB', party: 'PL'    },
  { name: 'Ciro Gomes',initials: 'CG', party: 'PDT'   },
  { name: 'Simone',    initials: 'ST', party: 'MDB'   },
];

function createCandidateCard({ name, initials, party }) {
  const card = document.createElement('div');
  card.className = 'candidate-card';
  card.setAttribute('role', 'button');
  card.setAttribute('tabindex', '0');
  card.setAttribute('aria-label', `Ver informações de ${name}`);

  card.innerHTML = `
    <div class="candidate-card__avatar">${initials}</div>
    <div class="candidate-card__name">${name}</div>
    <div class="candidate-card__party">${party}</div>
  `;

  // Clique: preenche o campo de busca com o nome do candidato
  const activate = () => {
    if (searchInput) {
      searchInput.value = `${name}: `;
      searchInput.focus();
      searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  };

  card.addEventListener('click', activate);
  card.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      activate();
    }
  });

  return card;
}

const grid = document.getElementById('candidatesGrid');
if (grid) {
  CANDIDATES_DATA.forEach((candidate) => {
    grid.appendChild(createCandidateCard(candidate));
  });
}

/* ── 5. SCROLL REVEAL (IntersectionObserver) ── */
const revealElements = document.querySelectorAll('.step, .candidate-card, .section-title, .section-subtitle');

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.15 }
);

revealElements.forEach((el) => {
  el.classList.add('reveal');
  revealObserver.observe(el);
});

/* ── 6. STEP: adiciona data-num via JS para manter HTML limpo ── */
document.querySelectorAll('.step__title').forEach((title, i) => {
  const num = String(i + 1).padStart(2, '0');
  title.setAttribute('data-num', num);
});
