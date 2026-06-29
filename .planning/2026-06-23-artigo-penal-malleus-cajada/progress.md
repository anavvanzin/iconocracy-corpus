# progress.md — Artigo de História do Direito Penal
Fase: 2026-06-23-artigo-penal-malleus-cajada
Working title: "Até quando duvidam, punem: o Malleus Maleficarum, Maria Gonçalves Cajada e a construção atlântica da suspeição inquisitorial de bruxaria"
Prazo: 30-jun-2026 (3 dias restantes em 27-jun-2026)

## Checkpoint 24-jun-2026 18:30 (fim da sessão)

## Checkpoint 26-jun-2026

- Bloqueio metodológico resolvido: o eixo deixou de ser "tipo penal" como categoria dogmática moderna e passou a ser "categoria de suspeição inquisitorial" / "figura penal-canônica".
- `Directorium Inquisitorum` (Eymerich; Peña) integrado como matriz procedimental anterior ao *Malleus*.
- Sbriccoli 2011 integrado em §2.4 para tratar a tortura como tecnologia intelectual de produção de verdade processual.
- Seção 5 rebaixada para interface em esboço: bruxa como figura punitiva da iconocracia, sem forçar o artigo a depender diretamente da tese.
- Seção 3 convertida de outline para prosa acadêmica: Cajada agora aparece como pivô documental, com mediação explícita de Cruz de Araújo/ANPUH, viés de seleção declarado e ponte clara para circulação atlântica.

## Checkpoint 27-jun-2026

- Dirty tree audit criado em `.planning/2026-06-27-dirty-tree-audit.md`, com classificação `keep`, `fold into docs`, `later` e `ignore/quarantine`.
- Planejamento DIR410346 alinhado ao artigo atual: Cajada tratada como pivô documental, não caso central; eixo metodológico fixado em suspeição inquisitorial, figura penal-canônica e procedimento.
- Seção 4 saneada em `artigo_v1_consolidado.md`: removida a referência não verificada a `Cães de Guarda`; adicionados Laura de Mello e Souza e o artigo de João José Reis sobre calundu; Angola e Goa rebaixadas para extensões comparativas, não prova central.
- `artigo_v0_consolidado.md` recebeu alinhamento mínimo da Seção 4 para não contradizer o v1.
- Próximo gate: validar schema 328 registros, rodar testes do validador, checar termos da tese, `diff --check` e busca dirigida por termos problemáticos nos arquivos ativos.

### Estado do artigo
- **artigo_v0_consolidado.md**: 6.448 palavras (começou o dia com 3.900 — +65%)
- Estrutura: resumo + introdução expandida (T3, T4) + 5 seções + conclusão + 20 referências ABNT

### ✅ Feito hoje (manhã — T1b + T2)
- Roper 2013, Cap. 1: lido, extraído, integrado no findings.md §3 e Seção 1
- 7 relatórios de fontes em sources/ (Roper, Levack, Behringer, ANPUH 2015, Cruz de Araújo 2017, Wikipedia Cajada, Wikipedia Malleus)
- findings.md expandido (§3, §5, §7, §8)

### ✅ Feito hoje (tarde — adiantamento de T3/T4 + integrações)

**T3 — Justificativa do pivô**: Seção "Por que Cajada é pivô, não caso central" na introdução (~400 palavras). Três argumentos + três negativas.

**T4 — Recorte temporal**: Seção "Por que 1487-1810" na introdução (~350 palavras). 1487 = estabilização doutrinária; 1810 = fechamento institucional; 1810 > 1821.

**Malleus Part III**: Questions XIII e XV citadas textualmente na Seção 2.2. Fonte: Mackay (2009). Source file: sources/malleus_part_III.md.

**Torre do Tombo**: Processo nº 10748 adicionado à Seção 3.

**Federici (Ideia 1)**: Seção 4.2 reescrita como "hibridização como acumulação primitiva do corpo feminino". Citações diretas de Federici (2004, pp. 11, 184): cercamentos, expropriação do corpo, figura da obeah caribenha. Conclusão ampliada com parágrafo Federici: "a bruxa de Estremoz e a escravizada de Salvador são produtos do mesmo regime de expropriação."

**Salazar Frías (Ideia 3)**: Contraponto Espanha × Portugal na Seção 2.1. Logroño 1609-1614: maior caça espanhola (1.384 crianças + 420 adultos). Salazar investiga, refuta o sabá, Instrucciones de 1614 acabam com fogueiras na Espanha. Enquanto Portugal produz Regimento de 1613 (codifica tortura). Mesmo Malleus, mesma cronologia, gramáticas institucionais opostas. Referência: Henningsen (1980).

**Hespanha (Ideia 2)**: Seção 1.3 expandida com 3 parágrafos. Três conceitos: (a) ordem plural corporativa do Antigo Regime (Hespanha 2018/2012); (b) fatos justiciáveis — por que maleficium, não sabbat; (c) economia da graça (Hespanha 2015). Explica estruturalmente o filtro ibérico do Malleus.

### Novos arquivos criados
- `plano_24jun.md`
- `sources/malleus_part_III.md`

### Novas referências adicionadas à bibliografia
- DAL RI JÚNIOR; SONTAG (2011) — História do Direito Penal entre Medievo e Modernidade
- HENNINGSEN (1980) — The Witches' Advocate
- HESPANHA (1994) — As vésperas do Leviathan
- HESPANHA (2015) — Como os juristas viam o mundo
- KRAMER; SPRENGER (1487/2009) — Malleus Maleficarum (ed. Mackay)
- MARTYN et al. (2018) — The Art of Law

### ResearchClaw
- `.venv-311` criado em `/Users/ana/Research/GitHub/AutoResearchClaw/` (Python 3.11.15)
- Config atualizado: `config-historia-penal-bruxaria.yaml` → OpenRouter + DeepSeek
- `.venv` original (3.9) preservado intacto
- **Bloqueador**: `OPENROUTER_API_KEY` precisa ser exportada no shell antes de rodar
- Comando para validar: `export OPENROUTER_API_KEY="sk-or-..." && cd /Users/ana/Research/GitHub/AutoResearchClaw && .venv-311/bin/researchclaw validate --config config-historia-penal-bruxaria.yaml`

---

## 📅 Próximos dias

| Dia | Tarefa | Status |
|---|---|---|
| 25-06 | Expansão Seções 1-2 (redação, ~6 pp. cada) | ⏳ Pendente |
| 26-06 | Expansão Seções 3-4 | ⏳ Pendente |
| 27-06 | Seção 5 + concatenação ABNT | ⏳ Pendente |
| 28-06 | Self-review + ajustes | ⏳ Pendente |
| 29-06 | Margem | ⏳ Pendente |
| 30-06 | ENTREGA | ⏳ Pendente |

T5 (revisão de outline) já foi absorvido — T3 e T4 adiantados, outline fechado.
Dia 25 é puramente redação: Seção 1 (Malleus como evento) e Seção 2 (tecnologia do corpo confitente) já têm esqueleto completo + fontes integradas.

---

## Para a próxima sessão

1. **Ler o artigo do ponto onde parou** — a estrutura está sólida, as fontes estão no lugar, é hora de escrever
2. **Seção 1**: abrir com a citação Roper (etimologia de femina = fe+minus) como epígrafe informal
3. **Seção 2**: o grosso já está escrito (Malleus Part III + Salazar Frías); expandir subseções 2.3 (segredo) e 2.4 (regulação da tortura)
4. **ResearchClaw**: se quiser rodar o parecer simulado, exportar OPENROUTER_API_KEY e rodar validate → run (estágio G)
5. **Word count atual**: 6.448. Meta: ~12.000-15.000 para v1 (30/06)

### Ideias restantes (não implementadas)
- **4** — Coda Dilma 2016 (1 frase na conclusão): "caça às bruxas" como tropo político contemporâneo
- **5** — Epígrafe Roper na abertura da Seção 1

---

## Decisões locked
- Pivô único (Cajada + historiografia Malleus)
- Interface ICONOCRACIA em esboço (expansão 14/07)
- Recorte 1487-1810
- Idioma PT-BR

## Meta
Artigo v1 para 30-jun, ~15-20 pp, PDF+DOCX, submissão lusófona.
