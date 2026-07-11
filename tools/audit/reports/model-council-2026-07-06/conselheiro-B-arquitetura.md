# Model Council B — Arquitetura Técnica: `corpus_to_argument.py`

**Fonte analisada:** [corpus_to_argument.py](https://raw.githubusercontent.com/anavvanzin/iconocracy-corpus/main/tools/audit/scripts/corpus_to_argument.py) — 585 linhas, lido integralmente para esta avaliação.

## 1. Fragilidade da extração atual — top 3 pontos frágeis

**(a) `extract_regime()` depende de string matching em prosa livre.** A função busca `"regime"` em `claim_text` de *qualquer* `interpretation`, sem checar `claim_type`. Se um registro contiver a palavra "regime" em outro sentido (ex.: "regime jurídico da moeda"), o regex captura ruído e `normalize_regime()` pode devolver um token não mapeado em `REGIME_NORM`, caindo silenciosamente em `.lower()` sem validação — produzindo rótulos de regime não canônicos que quebram o agrupamento em `regime_order`. **Correção:** mover `regime` para um campo estruturado explícito (`iconocode.regime` ou `claim_type == "regime_marker"`), eliminando o regex; usar um `Enum`/`Literal` fechado com validação em tempo de leitura.

**(b) `extract_iconological()` mistura hierarquia de prioridade com limiar arbitrário de tamanho (`len(text) > 40`).** Um texto de 41 caracteres genérico passa; um de 39 caracteres denso é descartado. Isso é heurística de comprimento, não de qualidade semântica — o próprio ponto que o enunciado identifica como frágil (`len(claim_text) > 60` para lacuna). **Correção:** substituir limiares de `len()` por verificação de `claim_type` presente + não-vazio, e reservar comprimento apenas como sinal secundário de "densidade" reportado no relatório de qualidade, não como filtro de inclusão/exclusão.

**(c) Fallback de referência ABNT gera citação sintética sem marcação de proveniência (`extract_abnt`, linhas 108-117).** Quando `abnt_citations` está vazio (55% dos casos), o script monta `"{TITLE}. {date}. Disponível em: {url}."` — uma citação ABNT *fabricada* pelo pipeline, indistinguível visualmente da citação real extraída. Isso viola diretamente a regra de rastreabilidade do projeto (nunca fabricar dados sem marcação). **Correção:** todo ABNT sintético deve carregar um marcador explícito, ex. `[ABNT AUTO-GERADA — VERIFICAR]`, e nunca ser tratado como fonte "pronta para citar" na tese.

## 2. As 141 lacunas monossilábicas

**(a) Detecção precisa:** o `has_full_panofsky()` atual usa `len(claim_text) > 60` como proxy de riqueza — funciona por acidente, não por design. Proponho detecção por *whitelist negativa*: marcar como monossilábico qualquer `claim_text` que, após normalização (lowercase, strip), seja membro de um conjunto fechado de tags conhecidas (`{"fundacional", "normativo", "militar", "contra-alegoria"}`) OU tenha contagem de tokens ≤ 2. Isso é robusto a mudanças de comprimento e não depende de um limiar mágico.

**(b) Placeholder informativo sem invenção:** ao invés do atual `"[LACUNA: interpretação iconológica ausente...]"` (que descarta informação disponível), montar o placeholder concatenando apenas campos verificados: motivos (`pre_iconographic[].motif`), `summary_evidence`, `date_hint`/`place_hint` e o próprio `claim_type` da tag curta. Exemplo de template: `"[LACUNA ICONOLÓGICA — tag disponível: '{tag}'. Motivos codificados: {motifs}. Evidência factual: {summary_evidence[:200]}. Requer expansão interpretativa antes do freeze.]"`. Isso preserva 100% de rastreabilidade — nada é inferido, apenas reorganizado.

**(c) Priorização automática:** gerar uma coluna `priority_score` = combinação de (i) presença/ausência de thumbnail, (ii) `confidence` do registro, (iii) papel do regime na argumentação do capítulo (registros do regime "fundacional" no corpus francês, núcleo do Cap. 3, priorizados sobre "pendente"). O script já produz uma tabela de apêndice (linhas 406-419) — bastaria adicionar coluna de score e ordenar por ela, substituindo a ordenação por data.

## 3. Pipeline de enriquecimento com LLM

Viável, mas com escopo estrito. Um LLM pode expandir uma tag monossilábica (`"fundacional"`) em prosa **desde que** todo o conteúdo factual injetado venha de campos existentes (`summary_evidence`, `motifs`, `date_hint`, `place_hint`) — nunca de conhecimento paramétrico do modelo sobre o objeto específico. Risco principal de alucinação: o LLM "sabe" história geral e pode inserir fatos plausíveis mas não verificados sobre a moeda/selo específico. **Salvaguardas obrigatórias:** (i) prompt fechado ("use apenas os campos abaixo; não adicione fatos externos"); (ii) todo texto gerado por LLM marcado com tag imutável `[TEXTO GERADO POR IA — REVISADO EM: ___]` até validação humana; (iii) validação humana obrigatória antes de qualquer uso em draft submetido — nunca migrar automaticamente para "sem lacuna"; (iv) log separado (`llm_enrichment_log.jsonl`) com prompt, resposta e modelo usado, para auditoria. Custo estimado: 141 registros × ~500 tokens de contexto + ~300 de saída ≈ 115k tokens totais — trivial (<US$ 2 mesmo em modelos premium tipo Claude Opus ou GPT-4 classe). O gargalo é a revisão humana, não o custo computacional.

## 4. Arquitetura Jinja2

A concatenação atual (`make_paragraph`, linhas 173-242) mistura lógica de extração, decisão condicional e formatação de string no mesmo bloco — qualquer mudança estilística exige editar Python. Migrar para Jinja2 separaria: (i) uma camada de extração/normalização (já existente, mantida em Python), que produz um dicionário limpo por registro; (ii) templates `.md.j2` por seção/regime (`template_fundacional.md.j2`, `template_lacuna.md.j2`), permitindo que a pesquisadora ajuste fraseado, ordem de frases ou tom por regime **sem tocar no código**. Isso também resolve a duplicação atual entre `_regime_intro_fr` (só para o modo `cap3`) e as demais funções `mode_*`, que reimplementam lógica similar de agrupamento — um único template parametrizado por `regime` cobriria todos os modos.

## 5. Versionamento e reprodutibilidade

Calcular um hash SHA-256 do `records.jsonl` completo (`sha256sum records.jsonl`) e gravá-lo no cabeçalho de cada documento gerado, junto com timestamp e contagem de registros — substituindo o atual `datetime.now()` isolado (linha 347), que não amarra o texto a uma versão específica dos dados. Um arquivo `corpus.lock.json` simples (`{"records_sha256": "...", "count": 328, "generated_at": "...", "script_version": "git commit hash"}`) versionado junto ao draft do Cap. 3 permite recriar exatamente o mesmo texto ou detectar divergência (`git diff` no lock acusa mudança de corpus mesmo que o texto pareça igual).

## Conclusão — 3 aprimoramentos de maior impacto, em ordem de implementação

1. **Substituir heurísticas de regex/comprimento por campos estruturados e whitelist fechada** (itens 1a, 1b, 2a) — é pré-requisito para tudo o resto; sem isso, qualquer camada adicional (Jinja2, LLM) herda os mesmos erros silenciosos.
2. **Marcação obrigatória e visível de todo conteúdo sintético/inferido** (ABNT fabricada, placeholders de lacuna, texto gerado por LLM) — protege a integridade acadêmica antes de qualquer automação adicional.
3. **Hash/lock de reprodutibilidade + migração para Jinja2** — uma vez que a extração é confiável e a proveniência é marcada, essas mudanças de manutenibilidade e rastreabilidade consolidam o pipeline para uso repetido ao longo da redação da tese.
