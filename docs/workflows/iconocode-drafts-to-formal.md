# Workflow — Drafts IconoCode → Codificação Formal

Como as análises visuais de IA (skill `iconocode-analyze`) alimentam a
codificação formal manual sem contaminá-la. Formaliza o fluxo usado desde
2026-07-02 (PRs #126/#128).

## Princípios

1. **Draft nunca vira codificação formal automaticamente.** O ledger
   `data/processed/purification.jsonl` só recebe entradas da sessão
   interativa (`code_purification.py`) ou de scripts auditados — `coded_by`
   registra quem decidiu.
2. **Só codificar o que se vê.** Drafts sem imagem acessível levam
   `#análise-textual` e `confidence_score` baixo; não promover à codificação
   formal antes de obter a imagem (norma estabelecida no PR #123).
3. **Draft é sugestão exibida, não default pré-preenchido.** Na sessão
   interativa a coder digita cada escore; a sugestão IA aparece ao lado,
   nunca é aceita por Enter.

## Fluxo

```
imagem/URL → skill iconocode-analyze (visão real)
        ↓
data/interim/iconocode-drafts/<lote>.json   ← 1 JSON por lote, commitado via PR
        ↓
python tools/scripts/code_purification.py --draft-file <lote>.json --item <chave>
        ↓  (Ana vê "draft IA sugere: N" por indicador e decide o dela)
data/processed/purification.jsonl           ← coded_by = humano
```

## Formato do arquivo de drafts

`{"drafts": [...]}` ou lista plana. Cada draft segue o schema do skill
`iconocode-analyze`: `id`, `draft_status`, `panofsky` (3 níveis),
`purificacao` (10 indicadores int 0–3, `purificacao_composto`,
`regime_iconocratico` minúsculo), `analyst_notes`, `coded_by`,
`confidence_score`. Exemplo real:
`data/interim/iconocode-drafts/iconocode-drafts-PR122-PR123-2026-07-02.json`.

## Resolução de identidade

`--item` e o casamento draft↔item aceitam **qualquer** chave — handle
XX-NNN, slug descritivo, SCOUT-NNN ou UUID — resolvidos via
`data/processed/id_crosswalk.jsonl` (`tools/scripts/id_crosswalk.py`).
Não há regime único de ID: handles são estáveis, nunca renomeados; UUID é a
chave de máquina (decisão de council, 2026-07-02, PR #128).

## Vault

Item com nota em `vault/candidatos/`: anexar a análise sob a seção
`## IconoCode Analysis (draft)` preservando o conteúdo existente (regra do
skill `iconocode-analyze`). Itens sem nota: o JSON do lote basta; criar nota
é opcional.

## Auditoria de drafts IA anteriores

Segunda passada independente (outro modelo/sessão) sobre codificações
`coded_by: iconocode-*` pendentes: gerar novo draft, comparar indicador a
indicador e registrar divergências no JSON (`audit_vs_*`). Divergência
documentada vale mais que concordância silenciosa — ver
`iconocode-drafts-PR122-PR123-2026-07-02.json` (auditoria dos itens
`iconocode-sonnet5` do PR #123).
