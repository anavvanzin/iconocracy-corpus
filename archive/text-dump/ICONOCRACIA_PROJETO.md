# Iconocracia — Projecto de Pesquisa no Gallica
## Índice de Recursos e Artefactos

---

## Resumo do Projecto

Pesquisa iconográfica para a tese **Iconocracia** (PPGAV/UFSC), explorando o acervo digital da Bibliothèque nationale de France (Gallica) para constituir dois corpora paralelos:

1. **Corpus francês**: Marianne — a alegoria feminina da República francesa (82 imagens indexadas por LPAI, 1871–1970)
2. **Corpus brasileiro**: programa visual do Apostolado Positivista do Brasil + iconografia imperial de Debret (a gramática visual que a República veio substituir)

---

## Ficheiros Guardados (Pasta de Outputs)

### 📄 Documentos de Pesquisa

| Ficheiro | Conteúdo | Linhas |
|---|---|---|
| `Debret_Vol3_Placas_Iconocracia.md` | Catálogo completo das pranchas relevantes do Vol. 3 do *Voyage pittoresque* com URLs IIIF de alta resolução | 127 |
| `Apostolado_Positivista_Programa_Iconografico.md` | Notas de pesquisa sobre o programa iconográfico positivista: bandeira, alegoria feminina (Clotilde de Vaux), Décio Villares, publicações primárias | 138 |
| `ICONOCRACIA_PROJETO.md` | Este ficheiro — índice geral do projecto | — |

### 🛠 Código (MCP Server)

| Recurso | Descrição |
|---|---|
| `gallica-mcp-server/` | Servidor MCP para acesso ao Gallica — **git init'd**, commit `9bd802f` |
| `gallica.plugin` | Plugin Cowork compilado (inclui o MCP server + skills Gallica) |

---

## Pranchas Debret — Resumo Rápido

Todas com alta resolução em: `https://gallica.bnf.fr/iiif/ark:/12148/btv1b8540997t/f{N}/full/1500,/0/native.jpg`

| Prancha | Página (f) | Tema | Relevância |
|---|---|---|---|
| **Pl. 10** | f301 | Regálias imperiais: coroa, cetro, orbe + todas as Ordens | ⭐⭐⭐ Os objectos físicos do poder que a República desfez |
| **Pl. 14** | f309 | Le Bando — Proclamação Municipal equestre | ⭐⭐ A palavra imperial performatizada |
| **Pl. 17** | f315 | Primeiras medalhas: Dom João VI e Dom Pedro I em perfil | ⭐⭐ Numismática como iconografia política |
| **Pl. 20** | f319 | Palácio de S. Cristóvão em 1808/1822/1831 | ⭐⭐ Espaço imperial como narrativa dinástica |
| **Pl. 22** | f323 | Guarda de Honra + Archeiros | ⭐ Corpos uniformizados do poder |
| **Pl. 37** | f351 | Aclamação de Dom João VI no salão do trono | ⭐⭐⭐ Gramática visual inaugural da monarquia americana |
| **Pl. 44** | f365 | Cortejo do Sacre / Procissão Real (exterior) | ⭐⭐ O lado público da coroação |
| **⭐ Pl. 48** | f373 | *Cérémonie du Sacre de D. Pedro 1er, 1er Décembre 1822* | ⭐⭐⭐ **A cena fundadora — contraponto directo da Proclamação** |
| **Pl. 51** | f379 | Aclamação de D. Pedro (I ou II) no Largo do Paço | ⭐⭐ Cerimónia de aclamação republicana |

---

## Corpus Marianne — Resumo Rápido

**Pesquisa Gallica:** `dc.subject all "Marianne" and dc.type any "image"`
**Total:** 82 imagens | **Período:** 1871–1970s | **Concentração:** 1894 (Steinlen) e 1914–1920 (propaganda WWI)

**Para recuperar o corpus:**
```
gallica_search(query='dc.subject all "Marianne"', document_type='image', limit=82)
```

---

## Programa Iconográfico Positivista — Achados-Chave

1. **Bandeira republicana** (19 nov. 1889): Teixeira Mendes + Miguel Lemos + Décio Villares
   Substituiu o brasão imperial por constelação astronómica + "Ordem e Progresso"

2. **Alegoria feminina positivista**: modelada sobre **Clotilde de Vaux** (musa de Comte) — europeia, contemplativa, casta
   ≠ Marianne (Liberdade combativa) ≠ índia/mulata (romantismo brasileiro)

3. **Décio Villares**: artista central — bandeira, monumentos, *Epopéia Africana no Brasil*

4. **Referência canónica**: José Murilo de Carvalho, *A formação das almas* (Companhia das Letras, 1990)

---

## MCP Server Gallica — Status

```
gallica-mcp-server/
├── src/            ← código fonte TypeScript (1,948 linhas)
│   ├── tools/      ← search.ts, image.ts, metadata.ts
│   └── services/   ← sru.ts, iiif.ts, oai.ts, client.ts
├── dist/           ← JavaScript compilado (pronto a usar)
├── README.md       ← documentação completa
└── .git/           ← repositório git (main branch, 1 commit)
```

**Para usar localmente:**
```bash
cd gallica-mcp-server
npm install
node dist/index.js   # stdio mode para Claude Desktop/Cowork
```

**Para publicar no GitHub:**
```bash
cd gallica-mcp-server
git remote add origin https://github.com/SEU_USUARIO/gallica-mcp-server.git
git push -u origin main
```

---

## Notas sobre Acesso ao Gallica

- **API IIIF funcionou**: todas as pranchas Debret acessíveis via `ark:/12148/btv1b8540997t`
- **API SRU funcionou**: pesquisas por assunto, tipo, data
- **API LPAI (iconografia)**: funcional mas não indexa iconografia republicana brasileira
- **Boletim do Apostolado (`cb32713468h`)**: registo de periódico — IIIF manifesto devolve 403; fascículos individuais nos. 27P–33P e 35P (1902–1905) disponíveis mas sem ARK directo encontrado
- **Gallica TLS issues** (20 mar. 2026): falhas intermitentes de TLS nas chamadas directas — usar o MCP server em sessões futuras

---

*Gerado em 20 de março de 2026 | Projecto Iconocracia | PPGAV/UFSC*
