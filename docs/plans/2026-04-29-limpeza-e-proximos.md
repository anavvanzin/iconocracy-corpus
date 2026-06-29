---
plano: "29-abril-2026 — Limpeza de drafts + próximos passos"
criado: 2026-04-29
status: em_andamento
---

# Plano — 29 de abril de 2026

## ✅ Fase 1 — Limpeza de IA nos 4 drafts (CONCLUÍDO)

Remoção de padrões "não X, mas Y" e outras muletas de IA em todos os rascunhos:

| Draft | Status |
|---|---|
| §3.2 — Contrato Racial Visual | ✅ limpo |
| §3.3 — Paternalismo jurídico-visual belga | ✅ limpo |
| Painel 1 — Corpo Vivo → Corpo Máquina | ✅ limpo |
| Painel 2 — Limiar da Dessexualização | ✅ limpo |

**Nota para a Ana:** Os "nãos" semanticamente necessários foram mantidos (ex.: "é estrutura, não acidente"). O que foi cortado é a muleta retórica "não se acumula como progressão lógica, mas se quebra como ruptura."

---

## 🟡 Fase 2 — Ana está revisando (EM ANDAMENTO)

- Ana lendo o Painel 2 (~2.100 palavras) e os demais drafts limpos
- Revisão crítica preparada para todos os 4 drafts

---

## ⏳ Fase 3 — Próximos passos (a disparar quando Ana autorizar)

### 3.1 — Aplicar correções estruturais apontadas na review
Cada draft tem pontos críticos (Rops no §3.2, seio no Educational Series, etc.). Aplicar após feedback da Ana.

### 3.2 — Painel 3 (Militar → Contra-alegoria)
Novo draft de painel do Atlas. Pode ser delegado.

### 3.3 — §3.4 (Rupturas e contra-alegorias)
Novo § do Capítulo 3. Pode ser delegado.

### 3.4 — Merge vault LPAI
Cópia rápida de `data/staging/vault-drafts-lpai-v2/` → `vault/candidatos/`. 10 vault notes.

### 3.5 — Compilar DOCX
`make docx` após Ana aprovar os rascunhos. C3 estabilizado no documento.

### 3.6 — Capítulo 4 (Desenho metodológico)
Começar quando C3 estiver maduro.

---

## 📝 Estratégia de delegação

Painel 3 e §3.4 são **independentes** — podem ser disparados em paralelo via `delegate_task` assim que a Ana der o sinal verde. Merge vault LPAI também roda em paralelo. Isso corta o tempo de espera pela metade.

---

## 💾 Infra

- Branch: `iconocracy-research-materials-clean`
- `origin` = SSD mirror (`/Volumes/ICONOCRACIA/git-mirrors/`)
- `github` = frio, sem CI/issues
- Último push: `2cfff31 feat(LPAI-v2): promote 10 items → ledger 175`
