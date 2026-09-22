# RELATÓRIO DE REVISÃO POR PARES (PEER REVIEW REPORT)

**Manuscrito:** Decisão metodológica: integração das alegorias de Virtudes, Continentes e Oceanos/Rios (Piloto v2)  
**Autor:** Codex (piloto v2 codebook)  
**Data:** 2026-06-22  

---

## AVALIAÇÃO GERAL (OVERALL ASSESSMENT)

### Contribuição (Contribution)
A decisão metodológica e a estruturação do [codebook-v2-alegorias.md](file:///Users/ana/Research/hub/iconocracy-corpus/docs/methodology/codebook-v2-alegorias.md) consolidam um avanço teórico fundamental para a tese *Iconocracia*. A inclusão de novas famílias alegóricas (Virtudes, Continentes e Oceanos/Rios) fornece a profundidade genealógica e o enquadramento geopolítico necessários para sustentar a hipótese da feminilidade de Estado sob a ótica da raça e da soberania territorial no Brasil. Ao adotar a premissa de Johanna Drucker (2011) e D'Ignazio & Klein (2020) de tratar os dados obtidos pela ferramenta LPAI v2 como *capta* (dados interpretativos e situados), o trabalho se alinha com as metodologias críticas contemporâneas das Humanidades Digitais.

### Pontos Fortes (Strengths)
1. **Rigor de Escopo**: A divisão estrita entre *corpus core* (estatal-jurídico brasileiro) e *comparador genealógico* (reproduções europeias ou apêndices de Ripa/Ortelius) mitiga eficazmente o risco de dispersão do objeto de estudo em uma história da arte genérica.
2. **Hipótese Racial Transversal**: A integração do campo `hipotese_racial` em todas as famílias impede a compartimentação do tema da colonialidade de gênero, tornando a raça uma variável analítica intrínseca a todo o corpus.
3. **Mapeamento Pragmático**: O roteiro de inserção nos capítulos da tese e o protocolo de decisão garantem a operacionalidade imediata das novas variáveis nas rotinas de escrita.

### Recomendação (Recommendation)
**Revisão Menor (Minor revision)**. O texto metodológico e as definições do codebook v2 são consistentes e prontos para aplicação piloto, necessitando apenas de pequenos refinamentos conceituais e ajustes de salvaguarda de metadados.

---

## ARGUMENTO (ARGUMENT)

### Clareza da Tese (Thesis clarity)
A tese de que o Estado nacional brasileiro herda, seculariza e racializa repertórios iconográficos de longa duração para legitimar sua soberania ("iconocracia tropical") é exposta com clareza. A distinção entre a América selvagem e a Efígie da República à romana expõe o nó entre gênero, raça e modernidade de forma impecável.

### Arco Argumentativo (Argumentative arc)
Conectado e coerente. Os três eixos articulam-se logicamente: a genealogia das virtudes legitima o tribunal/justiça (Eixo 1), a racialização das efígies define quem pertence à nação civilizada (Eixo 2) e a soberania hídrica e territorial demarca o espaço geográfico de poder (Eixo 3).

### Contradições Internas (Internal contradictions)
Nenhuma contradição conceitual detectada. O texto metodológico prevê de maneira satisfatória que, no caso de Oceanos e Rios (Eixo 3), a despersonalização ou masculinização de certos elementos (como no brasão da República) atua como um dado analítico "negativo" de valor igual ao enquadramento feminino purificado.

### Alegações Não Argumentadas (Asserted-but-not-argued claims)
* **Seção 2, Eixo 3**: A afirmação de que a despersonalização dos corpos d'água no Brasão republicano evita a "personificação imperial masculina" necessita de suporte documental posterior (ex.: debates na comissão de criação do brasão em 1889). Deve ser tratada como hipótese a testar no capítulo correspondente, não como fato assente.

---

## METODOLOGIA (METHODOLOGY)

### Declaração de Método (Method statement)
Adequada. A fusão entre iconografia jurídica e métodos computacionais (LPAI v2) está bem balizada.

### Adequação das Fontes (Evidence/source adequacy)
O piloto v2 de 1932 linhas demonstra robustez amostral para o teste. A inclusão de referências clássicas (Cesare Ripa, 1618; Marina Warner, 2000; Judith Resnik & Dennis Curtis, 2011; Ana Cecília de Souza, 2014) assegura o alinhamento historiográfico.

### Limitações Reconhecidas (Limitations acknowledged)
Sim. O risco de eurocentrismo é explicitamente tratado com a introdução da chave de metadados `subaltern_caution: true`.

---

## ENGAJAMENTO ACADÊMICO (SCHOLARLY ENGAGEMENT)

O engajamento com a literatura é substantivo. A citação a Resnik & Curtis (2011) ancora perfeitamente a seção sobre arquitetura forense, enquanto Souza (2014) e Warner (2000) sustentam as representações de Continentes e a purificação do corpo feminino de Estado. A adesão ao estilo ABNT NBR 6023:2025 está rigorosamente declarada no codebook.

---

## CONSISTÊNCIA INTERNA (CONSISTENCY)

### Terminologia e Definições (Terminology & Definitions)
O codebook define com rigor os novos termos de metadados (`familia_alegorica`, `subtipo`, `vetor_colonial`, `hipotese_racial`).

### Consistência do Sistema de Citação (Citation system)
Uniforme. A ortografia de nomes próprios (ex. *Ripa*, *Collaert*, *Ortelius*) e as datas de publicação das referências no codebook estão corretas.

---

## ALTERAÇÕES REQUERIDAS (REQUIRED CHANGES)

### [MAJOR]
1. **Refinamento Histórico-Documental (Eixo 3 - Rios/Oceanos)**: Na escrita do capítulo "Brasão e soberania", deve-se explicitar que a ausência de figuras antropomórficas (femininas ou masculinas) no brasão de 1889 difere do modelo imperial, e que a interpretação de que isso evita a "personificação imperial" deve ser justificada com base em fontes primárias republicanas (Decr. nº 4 de 1889).

### [MINOR]
1. **Verificação de Duplicatas no Ingest**: Assegurar que a integração do `piloto-v2-alegorias-final.json` ao ledger `records.jsonl` use IDs UUID únicos para evitar duplicação ou sobreposição de itens de dados que representam a mesma imagem física sob suportes diferentes.
2. **Consistência do Atributo `subaltern_caution`**: Nas diretrizes da ferramenta, reforçar que `subaltern_caution: true` deve ser obrigatoriamente registrado no campo correspondente sempre que uma representação de Continentes (América, África, Ásia) contiver atributos de selvageria, nudez parcial ou submissão colonial.
