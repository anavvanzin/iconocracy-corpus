# Vault Curation — Batch 1 (prioridade alta)

Data: 2026-04-17
Escopo: primeira triagem curatorial do backlog SCOUT de alta prioridade
Worktree: `/Users/ana/Research/.worktrees/iconocracy-corpus-hub-consistency`

## Lote inspecionado

- `SCOUT-406` — Alegorias do Palácio do Catete
- `SCOUT-204` — Proclamação da República (litografia de Angelo Agostini)
- `SCOUT-205` — Frontispício do Decreto n.º 1 (1889)
- `SCOUT-206` — Medalha comemorativa da Proclamação da República (1890)
- `SCOUT-423` — 50 Mil Réis, Banco do Brazil (1890)
- `SCOUT-415` — O mundo às avessas: voto feminino
- `SCOUT-321` — Statue of the Republic, Daniel Chester French (1893)

## Método desta passada

1. leitura integral das notas SCOUT
2. checagem se o URL já aparece no ledger atual (`records.jsonl`) — não aparece para nenhum dos 7 casos
3. tentativa de verificação externa dos URLs via web tools
   - falhou por erro de autorização das ferramentas web nesta sessão
4. decisão curatorial conservadora: só promover quando a rastreabilidade estiver suficientemente sólida

## Decisão por item

### SCOUT-406 — Alegorias do Palácio do Catete
Decisão: `PROMOVER (alta prioridade)`

Racional:
- relevância teórica excepcional para ENDURECIMENTO no Brasil
- vínculo claro com sede do poder executivo
- nota já documenta o evento crítico de substituição por águias
- URL é institucional (Museu da República) e a nota traz fonte complementar do próprio museu
- mesmo sem IIIF, a rastreabilidade está suficientemente acima da média do backlog

Pendências antes da promoção efetiva:
- idealmente fixar uma imagem/documento visual estável além do PDF
- confirmar data exata da remoção das alegorias

### SCOUT-204 — Proclamação da República (Agostini)
Decisão: `PROMOVER (alta prioridade)`

Racional:
- peça fundacional brasileira muito forte
- boa descrição visual
- articulação clara com Contrato Sexual Visual e regime fundacional
- rastreabilidade aceitável via Hemeroteca, ainda que sem IIIF

Pendências:
- substituir, quando possível, o hotpage por um link mais estável/preciso de imagem
- confirmar data completa e paginação final

### SCOUT-205 — Frontispício do Decreto n.º 1 (1889)
Decisão: `PROMOVER (muito alta prioridade)`

Racional:
- caso exemplar de acoplamento imagem-norma
- excelente encaixe metodológico no corpus
- peça quase “obrigatória” para o argumento da tese
- descrição visual já está madura o suficiente para entrar no ledger

Pendências:
- normalizar o URL do DocVirt se houver endpoint mais estável
- confirmar se existe imagem exportável de melhor qualidade

### SCOUT-321 — Statue of the Republic (Daniel Chester French)
Decisão: `PROMOVER (alta prioridade)`

Racional:
- fecha uma lacuna importante do registro monumental dos EUA
- URL do LOC parece plausível e a nota é consistente
- caso forte para Columbia/república monumental

Pendências:
- padronizar nota em português jurídico-histórico na passagem para o ledger
- confirmar metadados finais do item no LOC

### SCOUT-423 — 50 Mil Réis, Banco do Brazil (1890)
Decisão: `MANTER NO BACKLOG, MAS QUASE PRONTO`

Racional:
- iconograficamente muito promissor
- programa tripartido muito forte para a tese
- porém a fonte atual é catálogo privado / blog numismático
- rastreabilidade ainda insuficiente para promoção imediata sem uma segunda fonte mais sólida

Ação recomendada:
- buscar referência Pick / catálogo numismático mais estável ou acervo institucional
- só depois promover

### SCOUT-415 — O mundo às avessas: voto feminino
Decisão: `MANTER FORA DO LEDGER POSITIVO PRINCIPAL POR ENQUANTO`

Racional:
- item é extremamente importante
- mas ele funciona melhor como `contra-alegoria` / resistência iconográfica do que como entrada regular do corpus positivo
- merece provavelmente uma trilha própria de casos negativos, contra-alegóricos ou resistência visual

Ação recomendada:
- não descartar
- manter em subcorpus/registro de contra-alegorias ou criar lane específica antes da promoção

### SCOUT-206 — Medalha comemorativa da Proclamação da República (1890)
Decisão: `NÃO PROMOVER NESTA PASSADA`

Racional:
- a nota é boa, mas o URL atual (`.../obras/12345/...`) parece marcador frágil/dummy e precisa ser verificado
- sem confirmação externa confiável nesta sessão, a promoção seria arriscada

Ação recomendada:
- localizar URL institucional ou catálogo numismático verificável
- reavaliar no batch 2

## Resultado do batch 1

### Prontas para promoção em batch 2
- `SCOUT-205`
- `SCOUT-204`
- `SCOUT-321`
- `SCOUT-406`

### Quase prontas, mas dependem de fonte melhor
- `SCOUT-423`
- `SCOUT-206`

### Requer lane própria de curadoria
- `SCOUT-415`

## Próximo passo recomendado

Executar um `batch 2` de promoção canônica só com os 4 casos mais seguros:
1. `SCOUT-205`
2. `SCOUT-204`
3. `SCOUT-321`
4. `SCOUT-406`

Com isso, a curadoria avança sem contaminar o ledger com casos ainda frágeis.
