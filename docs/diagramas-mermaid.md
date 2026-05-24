# Diagramas Mermaid — ICONOCRACIA

Diagramas para colar no Notion/Obsidian (blocos de código Mermaid).

## 1. Diagrama Principal (flowchart)

```mermaid
flowchart TB
	A["Problema central<br>Presença alegórica feminina (Estado/Direito)<br>vs exclusão jurídica das mulheres reais"] --> B["Hipótese operacional<br>Regime iconocrático = tecnologia visual de legitimidade"]
	B --> C["Mecanismos"]
	B --> D["Dispositivos (suportes)"]
	B --> E["Eixos empíricos (o que medir/codificar)"]
	B --> F["Estratégia comparativa"]

	C --> C1["Simulacro<br>feminilidade estatal como efeito de circulação"]
	C --> C2["Purificação do corpo alegórico<br>idealização, assepsia, desmaterialização"]
	C --> C3["Reativação em crise/exceção<br>intensificação e deslocamentos formais"]

	D --> D1["Moedas e cédulas<br>ubiquidade íntima / repetição serial"]
	D --> D2["Selos e emblemas<br>circulação material do Estado"]
	D --> D3["Brasões e frontispícios normativos<br>autoridade simbólica"]
	D --> D4["Monumentos<br>verticalidade / permanência / pedagogia cívica"]
	D --> D5["Arquitetura forense e tribunais<br>teatralidade ritual do Direito"]

	E --> E1["Panofsky (3 níveis)<br>descrição / identificação / interpretação"]
	E --> E2["Ficha de codificação<br>suporte, atributos, postura, inscrição, local"]
	E --> E3["Regimes escópicos por suporte<br>ubíquo | monumental | ritual"]
	E --> E4["Evidência do paradoxo<br>reconhecimento simbólico sem reciprocidade política"]
	E --> E5["Imagem↔norma<br>vínculo com dispositivos legais coetâneos"]

	F --> F1["Caso-âncora: Brasil<br>República + Justiça nos espaços judiciais"]
	F --> F2["Contrastes: França (Marianne) | Reino Unido (Britannia)"]
	F --> F3["Conjunturas<br>guerras, rupturas institucionais, estados de exceção"]
```

## 2. Diagrama-Índice (mindmap)

```mermaid
mindmap
  root((ICONOCRACIA))
    Objeto
      Alegorias femininas
        Justiça
        República/Marianne
        Liberdade
        Britannia
    Paradoxo
      Presença imagética
      Exclusão jurídica
      "Contrato sexual visual"
    Corpus (suportes)
      Moedas
      Selos
      Brasões
      Monumentos
      Tribunais/arquitetura forense
      Paratextos normativos
    Método
      Panofsky (3 níveis)
      Codificação (ficha)
      Comparação transatlântica
      Imagem ↔ norma
    Lentes (clusters)
      Mondzain (economia do visível)
      Goodrich (emblemas jurídicos)
      Pateman (contrato sexual)
      Baudrillard (simulacro)
      Hegel (reconhecimento)
      Crary/Jay (regimes escópicos)
      Mary Douglas (pureza/perigo)
      Rancière (partilha do sensível)
      Butler (performatividade)
      Agamben (exceção)
    Saídas
      Estudos de caso
      Capítulos
      Banco de dados (DB1–DB12)
```

## 3. Subperguntas (graph)

```mermaid
graph TD
    PM[PERGUNTA MÃE] --> SP1[SP1: Quais figuras alegóricas<br/>BR 1822-1988?]
    PM --> SP2[SP2: Circulação de modelos<br/>europeus → Brasil]
    PM --> SP3[SP3: Estatuto jurídico<br/>das mulheres reais]
    PM --> SP4[SP4: Momentos de crise<br/>e iconoclasmo]
    PM --> SP5[SP5: Teoria feminista<br/>interpreta o paradoxo]
    PM --> SP6[SP6: Iconocracia tropical<br/>vs. europeia?]
```

## 4. Stack Tecnológico (flowchart)

```mermaid
graph LR
    A[Arquivo físico] -->|Fotografar| B[Tropy]
    B -->|Metadados imediatos| C[Airtable]
    C -->|Matriz completa| D[Codificação Iconclass]
    C -->|Export CSV semanal| E[Backup + QA]
    F[Bibliografia] -->|Gestão| G[Zotero]
    G -->|Citar| H[Escrita LaTeX/Word]
    C -.->|Opcional pós-defesa| I[Omeka S<br/>publicação online]
```

## 5. Cronograma (gantt)

```mermaid
gantt
    title Cronograma de Doutorado (24 meses)
    dateFormat YYYY-MM
    section Fundação
    Revisão bibliográfica + quadro teórico :2026-01, 3M
    Coleta documental (acervos BR)              :2026-04, 3M
    section Qualificação
    Escrita caps. teoria + 2 estudos caso BR    :2026-07, 6M
    QUALIFICAÇÃO                                :milestone, 2026-12, 0d
    section Expansão
    Coleta documental (acervos EU)              :2026-07, 3M
    Artigo 1 submetido                          :2026-09, 0d
    section Escrita
    Escrita caps. comparativos (FR, UK)         :2027-01, 6M
    Artigo 2 submetido                          :2027-04, 0d
    section Finalização
    Revisão integral + conclusão                :2027-07, 3M
    Revisão final + formatação                  :2027-10, 2M
    DEFESA                                      :milestone, 2027-12, 0d
```
