# ----------------------------------------------------------------------
# TESTES UNITÁRIOS (pytest) — funções puras, sem banco nem LLM
# ----------------------------------------------------------------------
# pytest                                        # rodar tudo (modo compacto)
# pytest -v                                     # ver cada teste com PASSED/FAILED
# pytest --collect-only -q                      # listar sem rodar
# pytest -v -k "brl"                            # filtrar por substring no nome
# pytest src/ai/tests/test_router.py -v         # rodar um arquivo só
# pytest -v 2>&1 | tee Docs/relatorios/testes_unitarios.txt

# ----------------------------------------------------------------------
# AVALIAÇÃO FUNCIONAL (run_eval) — pipeline end-to-end, precisa do FastAPI
# ----------------------------------------------------------------------
# .venv/bin/python src/ai/eval/run_eval.py
# .venv/bin/python src/ai/eval/run_eval.py --limit 8
# .venv/bin/python src/ai/eval/run_eval.py --tipo proposta

# ----------------------------------------------------------------------
# MÉTRICAS DO ROUTER — matriz de confusão + precisão/recall/F1 por classe
# Não precisa do FastAPI; só do .env com GROQ_API_KEY.
# ----------------------------------------------------------------------
# .venv/bin/python src/ai/eval/metrics_router.py --model 8b \
#     --json Docs/relatorios/metrics_router_8b.json
# .venv/bin/python src/ai/eval/metrics_router.py --model 70b \
#     --json Docs/relatorios/metrics_router_70b.json
# .venv/bin/python src/ai/eval/metrics_router.py --limit 8

# ----------------------------------------------------------------------
# MÉTRICAS DE RECUPERAÇÃO (RAG) — Hit@K, Recall@K, Precision@K
# Só precisa do banco rodando; não usa LLM.
# ----------------------------------------------------------------------
# .venv/bin/python src/ai/eval/metrics_retrieval.py \
#     --json Docs/relatorios/metrics_retrieval.json
# .venv/bin/python src/ai/eval/metrics_retrieval.py --k 1,5,10
