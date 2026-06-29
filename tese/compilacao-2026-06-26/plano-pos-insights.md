# Plano — Pós-Auditoria / Próximos Passos

**Data:** 2026-06-26 (noite)
**Contexto:** Auditoria 360° concluída (3 sprints). Artigo "Micro-Estado" ~11.200 palavras (7 seções). Corpus 80 itens.
**Insights da sessão:** 6 (subagentes, Colnect, escala, auditoria, selos, artigo)

---

## Horizonte imediato (próxima sessão — 27 jun)

### Bloco 1 — Finalizar o artigo (90 min)

- [ ] **Referências bibliográficas** — Rodar Elicit prompts REF-001 a REF-004 (codebook salvo em `prompt-codebook-elicit.md`)
- [ ] **Resumo + Abstract + Résumé** — 200 palavras cada, 5–6 keywords
- [ ] **Revisão de fluxo** — Ler artigo completo em sequência, verificar transições, consistência terminológica
- [ ] **Decidir nome final** — "Micro-Estado" vs. "O Estado no Bolso" vs. "Miniaturização e Soberania"
- [ ] **Decidir venue** — Law and Humanities / Visual Studies / Direito e Práxis

**Success criteria:** Artigo pronto pra submeter (só faltam refs + resumo + revisão)

### Bloco 2 — Expandir corpus de selos (60 min)

- [ ] **Abordagem alternativa ao Colnect** — O Anubis anti-bot bloqueou 5/7 tentativas. Explorar:
  - Wikipedia listas de selos por país (já funcionou pra Germania)
  - stampdata.com (usado com sucesso pelo subagente da Ibéria)
  - Catálogos postais nacionais (La Poste, Royal Mail, USPS)
  - API do Colnect? (verificar se existe acesso programático)
- [ ] **Meta:** +20 selos no corpus (68 → 88). Prioridade: Marianne anos 1940–60 (lacuna temporal)

**Success criteria:** +20 selos ingeridos, corpus 80 → 100

### Bloco 3 — Lacunas pendentes da auditoria (30 min)

- [ ] **Drive manifest** — Rebuild com id-mapping UUID (165→299 coverage)
- [ ] **3 PRs abertos** — #82, #108, #79: fechar ou merge?

**Success criteria:** Drive manifest ≥90% coverage. PRs resolvidos.

---

## Horizonte curto (esta semana)

### Bloco 4 — Submeter artigo (60 min)

- [ ] Formatação final (ABNT, figuras, tabelas)
- [ ] Cover letter
- [ ] Submissão

### Bloco 5 — Começar próximo artigo

- [ ] **Opção A:** "A Venda como Tecnologia de Gênero" (ideia #2 da brainstorm) — mais cirúrgico, 5.000 palavras
- [ ] **Opção B:** Iconometria Jurídica Comparada (artigo B do pipeline)
- [ ] **Opção C:** Nota Didática DIR410346 (artigo C)

---

## Anti-padrões aprendidos (NÃO repetir)

- ❌ Subagente fazendo scraping → timeout garantido (Colnect 5/5 falhas)
- ❌ `find -xtype l` no macOS → não funciona, usar `for + test ! -e`
- ❌ Commitar em branch errada → sempre verificar `git branch --show-current`
- ❌ `git push` sem `pull --rebase` → remote diverge (AGY pushando em paralelo)

## Padrões que FUNCIONAM (REPETIR)

- ✅ Parent faz pré-processamento de dados → injeta no context do subagente
- ✅ Subagentes de escrita pura (sem web calls) → 6/6 seções concluídas
- ✅ `while IFS= read -r -d ''` para arquivos com caracteres especiais
- ✅ Multi-wave parallel audit → 23 achados em 18 minutos
- ✅ `execute_code` para extrair estatísticas do corpus antes de delegar

---

## Métricas de sucesso da próxima sessão

- [ ] Artigo com referências + resumo + revisão de fluxo
- [ ] Corpus ≥100 itens
- [ ] Nome e venue decididos
- [ ] Tudo commitado e pushado
