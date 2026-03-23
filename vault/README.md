# Obsidian Vault — Iconocracia

Este é o vault Obsidian do projeto Iconocracia.

## Como abrir

1. Instale o [Obsidian](https://obsidian.md)
2. **Open folder as vault** → selecione esta pasta (`vault/`)
3. Instale os plugins recomendados quando solicitado:
   - **Dataview** — consultas sobre o corpus via frontmatter
   - **Templates** — fichas catalográficas padronizadas

## Estrutura

```
vault/
├── _templates/          ← Templates Obsidian
│   ├── ficha-catalografica.md
│   ├── nota-de-pesquisa.md
│   ├── capitulo.md
│   └── diario.md
├── corpus/              ← Fichas catalográficas do corpus
│   └── _index.md        ← MOC (Map of Content)
├── tese/                ← Capítulos da tese (Pandoc-ready)
│   ├── _sumario.md      ← MOC
│   ├── introducao.md
│   ├── capitulo-1.md ... capitulo-9.md
│   ├── conclusao.md
│   ├── references.bib   ← Bibliografia BibTeX
│   └── Makefile          ← Compilação Pandoc
├── pesquisa/            ← Notas de pesquisa
├── diario/              ← Diário de pesquisa
└── meta/                ← ADRs, codebook, metodologia
```

## Compilação com Pandoc

```bash
cd vault/tese
make docx         # Tese completa → output/tese_completa.docx
make pdf          # Tese completa → output/tese_completa.pdf
make capitulo-1.docx  # Capítulo individual
make setup        # Instruções de configuração
```

## Fluxo de trabalho

1. **Catalogar**: Crie ficha com template `ficha-catalografica` em `corpus/`
2. **Pesquisar**: Notas livres em `pesquisa/`, diário em `diario/`
3. **Escrever**: Capítulos em `tese/`, com wiki-links para fichas e notas
4. **Compilar**: `make docx` gera DOCX com citações ABNT
5. **Sincronizar**: `notion_sync.py` mantém Notion atualizado

## Plugins recomendados

| Plugin | Uso |
|--------|-----|
| Dataview | Consultas sobre o corpus (tabelas, listas, gráficos) |
| Templates | Inserção rápida de fichas e notas |
| Zotero Integration | Importação de referências do Zotero |
| Pandoc Reference List | Preview de citações no editor |
| Calendar | Navegação do diário de pesquisa |
