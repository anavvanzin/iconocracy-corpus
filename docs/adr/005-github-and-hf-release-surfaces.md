# ADR-005 — GitHub como Backbone Canônico e Hugging Face como Superfície Pública

**Data**: 2026-04-06  
**Status**: Aceito

## Contexto

O repositório vinha acumulando duas funções incompatíveis:

- ambiente operacional diário da tese
- trilha de backup automático em `main`

Ao mesmo tempo, o dataset público no Hugging Face já existia, mas estava
defasado em relação ao estado local do corpus. Era necessário separar
claramente:

- onde o trabalho é feito
- onde o histórico canônico é mantido
- onde as versões públicas são publicadas

## Decisão

### GitHub

GitHub passa a ser o **backbone canônico de colaboração e publicação**:

- `main` recebe apenas commits intencionais e legíveis
- branches curtas são o padrão de trabalho
- issues permanecem leves e limitadas a quatro fluxos:
  - corpus-expansion
  - purification-coding
  - thesis-writing
  - infra-publishing

### Hugging Face

Hugging Face passa a ser a **superfície pública de release**:

- `warholana/iconocracy-corpus` é um artefato de release
- snapshots são publicados em marcos relevantes, não a cada alteração local
- o primeiro Space é um explorador somente leitura, orientado ao dataset congelado

### Superfícies ativas

```
trabalho local  ->  GitHub canônico  ->  Hugging Face público
```

## Consequências

### Positivas

- `main` deixa de ser ruído de backup
- GitHub volta a ser útil para revisão e histórico
- Hugging Face recebe versões públicas coerentes e rastreáveis
- o primeiro demo público pode ser estável e não-interventivo

### Negativas

- backups automáticos precisam sair do fluxo padrão de commits
- publicar em Hugging Face passa a exigir uma etapa explícita de release
- qualquer divergência entre `records.jsonl` e `corpus-data.json` precisa ser tratada antes de release pública

## Regras operacionais

1. `records.jsonl` permanece a fonte canônica operacional.
2. `corpus-data.json` é o export público para sites e snapshots.
3. `purification.jsonl` é o ledger canônico de codificação.
4. `vault/candidatos/` é espelho auxiliar e não fonte pública.
5. Backups automáticos não devem ser commitados em `main`.
