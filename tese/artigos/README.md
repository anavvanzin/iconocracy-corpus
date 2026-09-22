# `tese/artigos/`

Rascunhos e revisões de artigos derivados da tese.

## Onde cada artigo mora

Decidido em 2026-08-15, após auditoria transversal
([`anavvanzin/artigos#1`](https://github.com/anavvanzin/artigos/pull/1)):

| Estágio | Casa canônica |
|---|---|
| Artigo pronto ou em revisão para submissão | **`anavvanzin/artigos`**, um diretório por artigo |
| Rascunho de trabalho, parecer, versão datada | **aqui**, com a data no nome |

A regra existe porque o mesmo artigo chegou a ter **três cópias idênticas** em
dois repositórios, sem nenhuma marcação de qual valia. Ao promover um rascunho
daqui para `artigos/`, remova a cópia solta e preserve apenas o snapshot datado
como registro histórico.

## Convenção de nomes

- `<slug>-draft-v<N>.md` — rascunho em elaboração
- `<slug>-rev.md` — revisão em curso
- `<slug>-peer-review-<AAAA-MM-DD>.md` — parecer
- `<slug>-<AAAA-MM-DD>/` — snapshot datado, congelado; não editar

## Compilação

Os artigos daqui são compilados pelo pipeline em `anavvanzin/artigos`:

```bash
# a partir do clone de anavvanzin/artigos, ao lado deste repositório
tools/compilar.sh --todos     # gera DOCX + PDF em out/
python3 tools/audit_artigos.py
```

Requer `pandoc` e `libreoffice-writer`.
