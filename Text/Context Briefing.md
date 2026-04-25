---
tags: [dialectic, briefing, metodologia, warburg, iconocracia]
aliases: [Context Briefing Atlas vs Score]
date: 2026-04-23
---

# Context Briefing: Atlas-based vs. Score-based Methodology for ICONOCRACIA

## Situacao da usuaria

Ana Vanzin, doutoranda em historia do direito com genero e artes (PPGD/UFSC). Tese: ICONOCRACIA — transformacao da alegoria feminina (Justitia, Libertas, Republica) de iconografia civica para imagetica estatal militarizada, seculos XIX-XX. Corpus atual: ~165 registros em `records.jsonl`, com indicadores de "endurecimento" (purificacao) numa escala ordinal 0-3. Sistema herdado de pipeline anterior (WebScout/IconoCode).

Ela esta stress-testando uma mudanca metodologica: abandonar a escala 0-3 em favor de uma abordagem "atlas-based" inspirada em Aby Warburg (Mnemosyne Atlas, Nachleben, pathos formulas).

## Paisagem do dominio

### Metodologia Warburgiana

- Aby Warburg (1866-1929): Mnemosyne Atlas = 79 paineis (placas) com fotografias de obras de arte, moedas, documentos, etc., dispostas nao linearmente.
- Eixo diacronico: Nachleben (sobrevivencia/afterlife) — formulas de pathos que retornam e se deformam ao longo do tempo, sem teleologia.
- Eixo sincronico: campo de forcas — imagens em relacao topologica, nao em sequencia historica linear.
- Warburg nao "classifica" imagens; ele as coloca em constelacao. Nao ha escala de valor, apenas rastros de sobrevivencia e contaminacao.
- Aplicacoes contemporaneas: digital humanities reconstruiram os paineis (Warburg Institute, Hamburg). Usado em iconografia politica (Horst Bredekamp), teoria da imagem (Georges Didi-Huberman, Philippe-Alain Michaud).
- Em direito/visual jurisprudence: Peter Goodrich (*Languages of Law*, *Legal Emblems and the Art of Law*) trabalha com imagetica juridica, emblemas, frontispicios. Costas Douzinas (*Law and the Image*) discute imagem e soberania. Bernhard J. Dotzler trabalha com midia e direito. NENHUM deles operationalizou um atlas Warburgiano como metodologia de tese — usam-no como referencia teorica ou hermeneutica, nao como estrutura analitica escalavel.
- Critica comum ao Warburg: anti-narrativo por design. Uma tese de doutorado precisa argumentar e demonstrar. O atlas e um Denkraum (espaco de pensamento), nao uma prova. O risco: a metodologia atlas vira estetica teorica que nao sustenta a exigencia demonstrativa da banca.

### Criticas a abordagens escalares em estudos visuais e de genero

- Feminist art history (Griselda Pollock, Rozsika Parker): a "classificacao" de imagens por criterios formais historicamente reproduz violencias epistemicas — o que e "degredado" ou "hardened" carrega julgamento estetico mascarado de neutralidade.
- Postcolonial studies (W.J.T. Mitchell, Nicholas Mirzoeff): reduzir imagens complexas a indices ou scores impoe teleologias coloniais de "progresso" vs. "decadencia".
- No caso especifico de alegoria feminina: quantificar "militarizacao" ou "perda de feminilidade" transforma o corpo feminino-signo em dado, reproduzindo a violencia que a tese quer analisar — a submissao da forma feminina a logica estatal racionalizada.
- Contudo: sem alguma forma de ordenacao/comparacao, como se opera com 165+ registros? O escore fornece legibilidade, comparabilidade transnacional, e um aparato de "rigor" que bancas de direito reconhecem.

### Projetos de atlas digital em humanities

- Mnemosyne digital (Warburg Institute): reconstrucao dos paineis, mas como arquivo curatorial, nao como ferramenta analitica de pesquisa com corpus proprio.
- Pelagios/Recogito, nodegoat: grafos de redes para dados historicos, mas nao especificamente para iconografia legal.
- PHAROS (photographic archive consortium): busca visual, mas nao estrutura atlas.
- Nao ha precedente claro de uma tese de historia do direito que use atlas warburgiano como metodologia central com corpus de 100+ imagens. Os exemplos existentes sao em historia da arte pura, e mesmo ali tendem a ser curadoriais/expositivos, nao demonstrativos.

## A tensao central

> [!warning] Atlas vs. Score
> **Atlas**: abandona teleologia, preserva contradicao, mapea Nachleben, e alinha com gender studies ao recusar a reducao do corpo feminino a metrica. Mas arrisca ser nao-operacional, nao-demonstrativo, e potencialmente ilegivel para uma banca de direito.
>
> **Score**: opera a escala do corpus, oferece rigor aparente, permite comparacao e generalizacao. Mas achata a complexidade visual, impoe uma narrativa linear de "endurecimento", e pode reproduzir a violencia epistemica que a tese critica (submeter a alegoria feminina a uma grade de avaliacao estatal/racional).

## Premissas ocultas a serem reveladas

1. Ambas as posicoes podem estar pressupondo que a metodologia deve ser UNICA (ou atlas ou score). A sintese pode ser uma terceira coisa, ou uma camada relacional.
2. Ambas podem estar pressupondo que a banca de direito exige QUANTIFICACAO como sinonimo de rigor. Isso e uma hipotese testavel.
3. A escala 0-3 foi herdada de um pipeline anterior (IconoCode/WebScout). Sera que ela representa uma conviccao teorica ou um acidente de infraestrutura?
4. A tese pode nao precisar que TODOS os 165 registros sejam tratados pelo mesmo aparato metodologico. Atlas e score podem operar em camadas diferentes.

## Sublimation Criteria (Preliminary)

- A sintese deve preservar a capacidade de operar com 165+ registros sem perder a nuance iconografica.
- Deve preservar a recusa feminista a reducao do corpo alegorico a metrica.
- Deve produzir um aparato demonstrativo que uma banca de direito possa reconhecer como rigoroso.
- Deve dissolver a suposicao de que atlas e score sao mutuamente exclusivos.

## Streams de pesquisa externa (Perplexity Deep Research)

Cinco streams de pesquisa foram compiladas em 23/04/2026 e estao disponiveis em `vault/dialectic/atlas-vs-score/streams/`:

1. **[[streams/stream1_warburg_legal\|Stream 1 — Warburg em iconografia juridica]]**: Stramignoni (2024) e o unico artigo em ingles que mobiliza *Pathosformel* na teoria da imagem juridica; Hayaert (2020) executa anatomia warburguiana de Justitia sem nomear Warburg; Becker (2013) aplica *Pathosformel* a Germania; Resnik & Curtis (2011) documentam que apenas 1 tribunal global representa Justitia como mulher nao-branca. **Lacuna estrutural confirmada**: nenhum trabalho combina Warburg + direito + feminismo + America Latina.

2. **[[streams/stream2_digital_atlases\|Stream 2 — Atlas digitais em cultura visual estatal]]**: NCRD (unica base de iconografia juridica) encerrou em 2021; modelos proximos sao Engramma (63 pranchas) e Erdteilallegorien (Viena, 407+ figuras, GIS, Iconclass). **Nao existe atlas digital dedicado a alegorias femininas no direito.**

3. **[[streams/stream3_scalar_critiques\|Stream 3 — Critica feminista/pos-colonial ao score]]**: Merry (2016) — indicadores juridicos *produzem* verdade em vez de revela-la; Haraway (1988) — o "truque-deus" do indice; Drucker (2011) — *all data is capta*; Espeland & Sauder (2007) — reatividade: indices disciplinam dados futuros; Warner (1985) — alegoria feminina e *constitutivamente paradoxal*, nenhum score suporta essa contradicao.

4. **[[streams/stream4_militarization\|Stream 4 — Militarizacao da alegoria civica feminina]]**: Padrao contra-intuitivo: militarizacao intensifica-se sob ruptura republicana, ameaca externa, expansao imperial; **atenua-se sob autoritarismo personalista** (Estado Novo prefere mae-Patria domestica a Republica armada).

5. **[[streams/stream5_synthesis\|Stream 5 — Sintese metodologica]]**: Didi-Huberman articula Warburg × Foucault; Pollock operationaliza atlas warburguiano como **dispositivo curatorial feminista contra-canonico** (Virtual Feminist Museum); Artl@s (Joyeux-Prunel) aplica Bourdieu cartograficamente; Andermann estende para America Latina.

Relatorio unificado: [[streams/iconocracia_atlas_research_report\|~9.600 palavras]].

## Ligacoes

- [[Monge A - Atlas Warburgiano\|Monge A — defesa do Atlas]]
- [[Monge B - Score 0-3\|Monge B — defesa do Score]]
- [[Index\|Voltar ao Index da sessao]]
