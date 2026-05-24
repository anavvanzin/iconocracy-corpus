# Anexo M.4 — Forma-arquivo vs. repertoire: a grade é constitutivamente iconocrática?

> **Executa:** Direção 3 da recursão (Fase 7, ciclo dialético 1).
> **Gatilho:** Monge B, §5 da revalidação — a *forma arquivo*, independentemente do conteúdo, codifica imagens em grades que matam polissemia. A condição ζ (Anexo M.2) não resolve; realiza o problema.
> **Data:** 2026-04-25.
> **Status:** Anexo investigativo — exige ciclo dialético próprio para decisão final. Aqui se reúne o material e se propõe uma resposta operacional.

---

## M.4.1 — O argumento de Monge B em termos rigorosos

Monge B não diz que o Atlas é bem ou mal feito. Diz que **a forma-arquivo é, por constituição, uma operação de poder**. Isso tem três camadas:

**Camada 1 — Seleccionar é governar.** Escolher quais imagens entram e quais ficam fora não é descrição — é governo do visível (Bennett, Foucault). O Atlas-topológico, mesmo critico, selecciona. A condição ζ não suspende esta operação: registra-a.

**Camada 2 — A grade produz o seu objecto.** A codificação LPAI não revela propriedades pré-existentes nas imagens — produz uma leitura que passa por objcetiva (Drucker: "data are capta, taken not given"). A grade LPAI v2 é uma *grade* no sentido literal: impõe coordenadas a um espaço que não as tinha.

**Camada 3 — A completude do arquivo é fantasmagórica.** Derrida (*Mal d'archive*): o arquivo fálico promete que o que foi archiving pode ser recuperado — mas a arquivização produz tanto quanto registra. O que não foi archivado não é perdido por acaso; foi excluido pela operación arquivística.

**A resposta de Monge A (não suficiente):** há arquivos que não governam assim — o arquivo-memorial (Alois Riegl), o arquivo-contrapúblico (Warner), o arquivo-monumento vandalizado (Young). A forma varia. A forma não determina por si só.

**O contra-argumento de Monge B (não refutado):** Taylor (2003) distingue *archive* de *repertoire* precisamente porque o archive é constitutivamente poder — o *repertoire* é onde o que não cabe no arquivo acontece: oralidade, performance, gesto. Se Pollock (*Virtual Feminist Museum*) parece ser um contra-exemplo (atlas como repertoire), é porque o *repertoire* do feminismo negro já estava lá antes do museum existir — o museum apenas o fotografou.

---

## M.4.2 — Taylor (2003) em detalhe: a distinção operativa

Taylor, *The Archive and the Repertoire*:

- **Archive:** sistema de inscriptions — textos, documentos, artefactos — que sobrevive no tempo e pode ser acumulado. O arquivo é o que resta. Opera por acumulação, seleção, preservação.

- **Repertoire:** repertório deledgeable — gestos, oralidades, performances — que existe apenas no presente do seu exercício e requer presença corporizada para ser transmitido. O répertoire não se arquiva; repete-se. Opera por diferença, não por acumulação.

A consequência para o Atlas-topológico:

O atlas é, por definição, archive. Ele recolhe imagens, fixa-as em pranchas, impõe vizinhanças. Não há atlas que seja puramente repertoire — porque repertorio exige presença viva, e o atlas é exactamente o dispositivo que separa a imagem do seu presente de uso.

O que Taylor permite, porém, é que o archive seja **aberto** pelo repertoire: que a presença de quem lê, performs ou testemunha altere o que o archive significa. Não que o substitua — que o abra.

---

## M.4.3 — A resposta operacional: archive + repertoire, não archive *ou* repertoire

### Proposta M.4

O Atlas-topológico da tese Vanzin não precisa deixar de ser archive para ser contra-iconocrático. Precisa ser **archive + repertoire**.

O archive (as pranchas, o LPAI, o corpus, os registros) faz o trabalho de documentação. O repertoire (testemunhos, performances de leitura, gestos de testemunhagem) faz o trabalho que o archive não consegue: expõe a violência do archive sem fingir que pode evitá-la.

A resposta de Hartman (2008, *Venus in Two Acts*) é aqui o modelo: ela não sai do arquivo colonial — entra nele com as testemunhas que ele excluiu, e diz o que foi feito. O que importa não é o que Hartman encontrou no arquivo; é o que ela diz *a partir de dentro*, sabendo que continua dentro.

### Componentes de repertoire a incluir na tese

**1. Testemunhos orais (componente ζ-plus)**

Os itens 166–169 (artefatos publicacionais da própria tese) são archive. Ao lado de cada um, incluir:

- Testemunho gravado (áudio, min. 3) de pessoa atingida pela iconocracia que a tese analisa — não acadêmica, não colega — lendo ou reagindo ao item codificado.
- Transcrição como item 170 (e seguintes) no corpus.
- Campo `testemunho_repertoire` em `records.jsonl` — diferente de `codificacao_lpai`.

**2. Performance de leitura em grupo (componente β-plus)**

A carta de endereçamento (condição β, Anexo M.2) não é apenas uma lista. É uma sessão de leitura coletiva onde comunidades nomeadas leem pranchas com a autora. O que resulta não é publicação académica — é registro de como o atlas foi recebido por quem ele pretende servir.

**3. Modo de apresentação oral (não apenas escrito)**

Quando a tese é apresentada em banca, seminário ou publicação oral, o formato inclui:
- Leitura de trecho de testimonio de item codificado.
- Momento de registro de reação da audiência.
- Inclusão da reacción como nota no corpus.

**4. Cartografia social como repertoire (componente δ-plus)**

Para o memorial técnico (condição δ, Anexo M.2): em vez de apenas aplicar a tese a um processo, fazer mapa social com comunidade atingida — o mapa é repertoire (existe no processo colectivo, não no documento).

---

## M.4.4 — Consequência para ζ (Anexo M.2)

A condição ζ original diz: "itens 166–169 no corpus, codificados pela grade LPAI v2 — **mapeia captura, não a impede**."

A versão M.4-plus diz: "itens 166–169 no corpus, archive + repertoire. O archive codifica. O repertoire testimunha. O que emerge da tensão entre os dois é o que Monge B pediu para assinar: não a resolução da captura, mas a sua exposição sem disfarce."

**O que muda nos indicadores ζ:**

| Indicador original | Indicador M.4-plus |
|---|---|
| Código LPAI v2 nos itens 166–169 | Código LPAI + campo `testemunho_repertoire` |
| Auto-codificação pela grade | Testemunhas (min. 3) lendo itens antes da publicação |
| Nenhum mecanismo de presença viva | Sessão de leitura coletiva registrada como item 170 |
| — | Transcrição de testemunho como item 171 |

---

## M.4.5 — O que não resolve (limites do M.4)

1. **Pollock é contra-exemplo real?** A tese assume que o Virtual Feminist Museum é archive + repertoire (não apenas archive). Isso precisa de verificação mais aprofundada. Uma visitante do VFM é convidada a performing ou a navegar? A diferença importa.

2. **Taylor em contexto brasileiro?** O concepto de repertoire de Taylor foi desenvolvido para contextos de performance afro-americana. A sua aplicação ao contexto brasileiro exige verificação — as comunidades negras brasileiras têm tradições de repertorio que Taylor não contemplou? Carnaval? Candomblé? A resposta não é trivial.

3. **A forma-arquivo permanece problema para quem não pode participar do repertoire.** Se o repertoire exige presença corporizada, quem não pode estar presente (por distância, por situação de invisibilidade forçada, por não ser welcome em espaços onde o atlas é apresentado) está excluído do que o archive não alcança. A inclusão do repertoire não resolve este problema — apenas o nomeia.

---

## M.4.6 — Material de bibliography para ciclo dialético próprio

### Fontes centrais

- TAYLOR, Diana. *The Archive and the Repertoire: Performing Cultural Memory in the Americas*. Durham: Duke UP, 2003.
- HARTMAN, Saidiya. Venus in Two Acts. *Small Axe*, v. 12, n. 2, p. 1–14, 2008.
- AZOULAY, Ariella. *Potential History: Unlearning Imperialism*. London: Verso, 2019. Cap. 4: "Archival Abjection."
- MBEMBE, Achille. The Power of the Archive and its Limits. In: HAMILTON *et al.* (orgs.). *Refiguring the Archive*. Dordrecht: Kluwer, 2002.
- STEEDMAN, Carolyn. *Dust: The Archive and Cultural History*. Manchester: Manchester UP, 2001.
- DERRIDA, Jacques. *Mal d'archive*. Paris: Galilée, 1995. Tradução: *Archive Fever*. Chicago: UCP, 1996.
- FOSTER, Hal. An Archival Impulse. *October*, v. 110, p. 3–22, 2004.

### Fontes complementares

- POLLOCK, Griselda. *Encounters in the Virtual Feminist Museum*. Routledge, 2007.
- BENNETT, Tony. *The Birth of the Museum*. Routledge, 1995.
- CONNOLLY, William. *Pluralism*. Durham: Duke UP, 2005. (Cap. sobre "creole performance" no Brasil)

---

## M.4.7 — Risco se não executada

Monge B tem razão em seu argumento sobre a forma-arquivo, e a síntese v6 não a refuta — a reduz a limite declarado. A condição ζ, sem este anexo, é o que o auditor chamou de "laudo pericial assinado pelo réu" no modo archive: codifica a si mesma e chama isso de reflexividade.

Com M.4-plus, ζ ganha o que Monge B pediu: não solução da captura, mas **exposição sem disfarce**. É o que Hartman faz — não sai do arquivo; entra com as testemunhas que ele excluiu.

---

*Documento produced as Direction 3 da recursão (Fase 7). Próximo passo: ciclo dialético completo ciclo 2 sobre archive vs. repertoire, a executar antes da defesa.*
