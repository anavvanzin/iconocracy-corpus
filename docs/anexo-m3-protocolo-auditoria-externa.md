# Anexo M.3 — Protocolo de Auditoria Externa com Poder Real

> **Executa:** Direção 2 da recursão (Fase 7, ciclo dialético 1).
> **Gatilho:** Ataque 1 da auditora hostil — sem mecanismo institucional real, α–ζ são *laudo pericial assinado pelo réu*.
> **Data:** 2026-04-25.
> **Status:** Rascunho operacional — exige negociação institucional real antes da defesa.

---

## M.3.1 — Preâmbulo: por que o que existe não basta

A versão v6 das seis condições α–ζ prevê "auditabilidade". A versão v6-reparada (Anexo M.2) declara que "sem auditores com poder institucional de recusa, α–ζ são laudo pericial assinado pelo réu". Esta declaração é retórica forte — mas exige operacionalização.

O que não basta:

- **Peer review da banca** — a banca é o circuito PPGD/UFSC; não é externa. O regime iconocrático que a tese estuda é reproduzido pela universidade que a abriga (Mbembe 2002; Stoler 2009). A banca avalia a tese que denuncia o regime que avalia a tese.
- **Declaração de limitações** — o Anexo M.2 já declara três limites; declaração sem mecanismo é o que o Ataque 1 chamou de "teatro de auto-absolvição".
- **Código aberto + PRs aceitos** — PRs são instrumentos de correção de código, não de recusa política. Um PR pode corrigir um erro de digitação; não pode recusar uma codificação que comunidades endereçadas consideram violenta.

O que se exige: instância(s) externa(s) ao circuito PPGD/CAPES/banca com **poder declarado de recusa** sobre pelo menos: (a) itens do corpus, (b) vocabulário de codificação, (c) narrativa da tese.

---

## M.3.2 — Auditores: nomeação concreta, tipo e escopo

### Princípio de nomeação

Os auditores são nomeados por **capacidade institucional de recusa**, não por interesse acadêmico. Recusa política exige coletivo com existência organizacional própria — não indivíduo consultores.

### Tipo 1 — Auditoria Comunitária Negra (ACN)

**Natureza:** organização de mulheres negras com existência federativa e independência do circuito acadêmico.

**Candidatas empíricas (a contatar, não a presumir):**
- **Geledés — Instituto Afro-Brasileiro** (São Paulo) — histórico em combate ao racismo e à violência de gênero; não é academia.
- **Cfemea — Centro Feminista de Estudos e Assessoria** (Brasília) — feminist theory-in-practice; participação em políticas públicas.
- **Coordenação Nacional de Articulação das Comunidades Negras Rurais — CONAQ** — para itens de alegoria agrária.
- **Marcha Mundial das Mulheres — MMM** (nível Brasil) — feminismo autônomo, não universitário.

**Poder:** Refusa items e vocabulários. Pode vetar a inclusão de um item no corpus ou a codificação de um atributo se considerar que reproduz ou掩饰a violência iconocrática.

**O que não pode:** Não pode escrever a codificação alternativa — pode recusar a existente, exigindo nova rounds de codificação com participação comunitária.

**Escopo:** Todos os itens do corpus brasileiro (eixo central da tese); itens de outros países onde a alegoria envolve corpos negros ou indígenas.

**Forma de recusa:** Registro formal (e-mail institucional ou carta) com justificativa, anexado ao registro do item em `records.jsonl` como campo `audit_refusal`.

---

### Tipo 2 — Auditoria de Especialistas Externos (AEE)

**Natureza:** profissionais com expertise fora do campo jurídico e da UFSC.

**Candidatas:**
- **ABRAJI — Associação Brasileira de Jornalismo Investigativo** — para a dimensão de arquivo jornalístico e direito à informação; já trabalharam com arquivos de violência institucional.
- **Museu Afro-Brasileiro de São Paulo (MAB)** — para a dimensão de memória e patrimônio negro; curadoria comunitária.
- **Centro de Documentação e Memória da Comissão Nacional da Verdade (CDMN/CNV)** — para arquivos de violação de direitos humanos; expertise em arquivos de violência de Estado.
- **Laboratório de Antropologia Jurídica da UFSC (LAJ-UFSC)** — anthropologists working on law outside doctrinal legal studies; deve ter ao menos 50% de membros sem vínculo com o PPGD/Direito.
- **Comitê de Ética em Pesquisa com Seres Humanos (CEPSH-UFSC)** — desde que incluya representação externa (não apenas professores da universidade).

**Poder:** Refusa métodos e narrativas. Pode considerar que o aparato metodológico (LPAI + Atlas) reproduz o problema que alega analisar, e recusar a publication como válido.

**Escopo:** Capta methodology e narrativa da tese — não itens individuais do corpus (esse é o escopo da ACN).

**Forma de recusa:** Parecer técnico formal, anexado ao documento da tese.

---

### Tipo 3 — Auditoria Cruzada Internacional (ACI)

**Natureza:** colaboração formal com outro atlas de alegorias jurídicas.

**Candidata:**
- **Erdteilallegorien Wien** (Universität Wien / Institut für Kunstgeschichte) — atlas digital de alegorias territoriais com 400+ figuras, Iconclass completo, código aberto. Contato: Prof. Dr. [a identificar]. Projeto com interface digital semelhante ao que Vanzin propõe; diálogo simétrico possível.

**Poder:** Refusa a claims epistemológicos. Pode considerar que o "Atlas-topológico" não é diferente do Erdteilallegorien em termos de operação de poder, e que a tese perde a reivindicação de diferença estrutural.

**Escopo:** A claim epistemológica central da tese — que o Atlas-topológico constitui arranjo difractivo-declarativo (cf. Anexo M.2, α). A ACI não audita itens individuais.

**Forma de recusa:** Joint statement assinando por ambas as partes, publicado no repositório.

---

## M.3.3 — Consequências operacionais de recusa

Quando qualquer auditor recusa:

| Nível de recusa | Item afetado | Consequência operacional |
|---|---|---|
| ACN: recusa de item | Item específico no corpus | Campo `audit_status` = `"contestada"`; item **não contado** na contagem final de validação; comunidade nomeadora recebe resposta em 60 dias com possibilidade de re-codificação coletiva |
| ACN: recusa de vocabulário | Atributo LPAI ou categoria | Atributo marcado `contested` no codebook; nova rounds de codificação com participação de representante da organização; mudança documentada no changelog |
| AEE: recusa de método | Atlas-topológico ou LPAI | Publicação da tese **adiada** até nova rodada de diseño metodológico com consultoria externa; defesa não pode ocorrer com recusa ativa pendente |
| ACI: recusa de claim | Reivindicação de diferença epistêmica | Reivindicação removida da tese ou reescrita com modificação substantiva; Erdteilallegorien pode co-assinar nova formulação ou recusar associação |

**Regra de desbloqueio:** qualquer recusa pode ser desbloqueada mediante nueva rounds de trabajo com participação do auditor que recusou. Não basta "revisar" — exige demonstração de que a objeção foi incorporada.

---

## M.3.4 — Ciclo de revisão

### Revisão ordinária (trimestral durante a pesquisa)

1. ACN recebe relatório trimestral com novos itens codificados.
2. AEE recebe versão draft do capítulo metodológico a cada revisão de orientação.
3. ACI recebe atualização anual sobre o estado do corpus.

### Revisão extraordinária (acionada por qualquer auditor)

- Qualquer auditor pode acionar revisão extraordinária se considerar que: (a) um item causa dano reputacional ou político a comunidades; (b) a tese reproduz iconocracia em vez de analisá-la; (c) houve mudança substancial no contexto institucional.
- Prazo para resposta da autora: 30 dias úteis.
- Prazo para protocolo de resolução: 90 dias.

### Revisão pré-defesa (obrigatória)

60 dias antes da defesa:
- ACN recebe versão completa da tese para leitura final.
- AEE recebe capítulo metodológico e anexo de resultados.
- ACI recebe seção de contribuição epistemológica.

**Se qualquer auditor registra recusa ativa no prazo de 60 dias pré-defesa:** defesa adiada até resolução. Esta é a condição Limite 1 do Anexo M.2 — sem ela, a tese não pode claimar que as condições α–ζ foram auditadas.

---

## M.3.5 — Limites declarados

1. **Este protocolo não resolve o Ataque 5 da Fase 6** — a tese continua sendo produzida dentro do PPGD/UFSC. O protocolo mitiga, não elimina.
2. **A negociação com auditores reais pode levar meses** — iniciar o contato o quanto antes. Mínimo viável: ACN (Geledés ou Cfemea) + uma AEE (ABRAJI ou CEPSH) antes da defesa.
3. **A ACI depende de外交** — o contato com Erdteilallegorien Wien exige projeto formal de colaboração; mínimo possível: intercâmbio de pareceres por e-mail com согласия mútua.
4. **Se nenhum auditor aceitar** — a tese declara a recusa como dado e publica com nota de auditoria recusada; não é possível fazer de outra forma.

---

## M.3.6 — Referências de suporte

- Mbembe, Achille. The Power of the Archive. *Refiguring the Archive*, 2002.
- Stoler, Ann Laura. *Along the Archival Grain*. Princeton UP, 2009.
- Azoulay, Ariella. *Potential History*. Verso, 2019.
- Kilomba, Grada. *Plantation Memories*. Unrast, 2008.
- Ataque 1, auditora hostil (Fase 6, cycling 1): `docs/dialectic-cycle-1/05-fase6-auditor-hostil.md`
- Síntese v6: `docs/dialectic-cycle-1/07-sintese-final-v6.md`

---

*Documento produced as Direction 2 da recursão (Fase 7). Requires real institutional negotiation; texto is framework only.*
