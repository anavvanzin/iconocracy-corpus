# Codebook v1 — Iconocracia
## Protocolo de Codificação do Corpus

**Versão:** 1.0 — junho 2026
**Changelog:** versão inicial; gerada a partir de notas de trabalho acumuladas e revisão do projeto v2.

---

## Sistema de Identificação

Cada item recebe um ID único no formato:

```
[PAÍS]-[SUPORTE]-[NÚMERO SEQUENCIAL]
```

**Códigos de país:** BRA · FRA · GBR · ESP · USA  
**Códigos de suporte:** MOE (moeda) · SEL (selo) · BRA (brasão) · MON (monumento) · ARQ (arquitetura forense) · PAR (paratexto normativo) · OUT (outro)

**Exemplo:** `BRA-MOE-001` = primeiro item brasileiro de suporte moeda.

---

## Ficha de Codificação

### Bloco A — Identificação

| Campo | Código | Instrução |
|---|---|---|
| ID do item | `A01` | Código único conforme sistema acima |
| Título / denominação | `A02` | Nome oficial ou denominação descritiva |
| País / jurisdição | `A03` | País emissor ou jurisdição de origem |
| Data de produção | `A04` | Ano ou intervalo; usar "c." para datas aproximadas |
| Suporte | `A05` | Categoria conforme códigos acima |
| Instituição emissora | `A06` | Ex.: Casa da Moeda, Correios, Tribunal de Justiça |
| Localização atual | `A07` | Museu, coleção, arquivo, ou "circulação" |
| Fonte da imagem | `A08` | URL, arquivo, referência bibliográfica |
| Classificação corpus | `A09` | Core / Comparador / Apêndice |

---

### Bloco B — Figura Alegórica

| Campo | Código | Instrução |
|---|---|---|
| Identificação da figura | `B01` | Nome da personificação (ex.: República, Justiça, Verdade) |
| Repertório | `B02` | Virtudes / Continentes / Oceanos-Rios / Estatal-Republicano / Outro |
| Fonte iconográfica identificável | `B03` | Ripa (edição/ano) / tradição local / inovação do artista |
| Postura corporal | `B04` | Em pé / sentada / em movimento / busto / outro |
| Orientação | `B05` | Frontal / perfil direito / perfil esquerdo / três-quartos |
| Expressão facial | `B06` | Serena / severa / majestosa / indeterminada |

---

### Bloco C — Marcadores de Gênero, Raça e Corpo

| Campo | Código | Instrução |
|---|---|---|
| Gênero da figura | `C01` | Feminino / Masculino / Neutro / Indeterminado |
| Fenótipo / marcadores raciais | `C02` | Descrição dos traços; usar categorias descritivas, não classificatórias |
| Tipo corporal | `C03` | Clássico-greco-romano / indígena / híbrido / estilizado / outro |
| Vestimenta | `C04` | Toga / túnica / traje nacional / alegórico / outro |
| Cabelos | `C05` | Soltos / presos / coroados / véu / outro |
| Seios expostos | `C06` | Sim / Não / Parcial |
| Atributos portados | `C07` | Lista: balança, espada, fasces, tocha, olivo, phrygian cap, lança, escudo, etc. |
| Inscrição ou legenda associada | `C08` | Texto completo se presente |

---

### Bloco D — Circulação, Uso e Ritual

| Campo | Código | Instrução |
|---|---|---|
| Contexto de uso primário | `D01` | Circulação monetária / correspondência / espaço público / judicial / legislativo |
| Alcance de circulação | `D02` | Nacional / regional / local / colonial / internacional |
| Público-alvo presumido | `D03` | Geral / letrado / jurídico / político |
| Reativação em contexto de crise | `D04` | Sim (descrever) / Não / Indeterminado |
| Relação com norma jurídica | `D05` | Paratexto de lei / brasão oficial / moeda legal / outro |

---

### Bloco E — Conflito de Imagens

| Campo | Código | Instrução |
|---|---|---|
| Registro de iconoclasmo | `E01` | Sim / Não |
| Tipo de conflito | `E02` | Destruição física / vandalização / substituição / protesto / reapropriação |
| Agente do conflito | `E03` | Estado / movimento social / indivíduo / indeterminado |
| Data do conflito | `E04` | Ano ou período |
| Resultado | `E05` | Imagem removida / restaurada / substituída / permanece contestada |
| Fonte do registro | `E06` | Referência bibliográfica ou documental |

---

### Bloco F — Análise Iconológica

**Atenção:** este bloco só é preenchido após o freeze do dataset. Nenhuma inferência antes do congelamento do corpus.

| Campo | Código | Instrução |
|---|---|---|
| Nível pré-iconográfico | `F01` | Descrição formal: o que se vê (formas, cores, linhas) |
| Nível iconográfico | `F02` | Identificação dos temas e convenções (Panofsky II) |
| Nível iconológico | `F03` | Interpretação dos significados intrínsecos (Panofsky III) |
| Relação com hipótese central | `F04` | Como este item evidencia, qualifica ou tensiona a hipótese |
| Notas do codificador | `F05` | Dúvidas, incertezas, necessidade de segunda opinião |

---

## Campos Diferenciados por Repertório

### Repertório: Virtudes (Bloco G-V)

Aplicar quando `B02 = Virtudes`

| Campo | Código | Instrução |
|---|---|---|
| Virtude específica | `GV01` | Justiça / Prudência / Fortaleza / Temperança / Verdade / Paz / Concórdia / Fé / Esperança / Caridade / Outra |
| Atributos canônicos presentes | `GV02` | Conforme Ripa: ex. Justiça = balança + espada; listar os presentes |
| Desvios do cânone de Ripa | `GV03` | Quais atributos foram omitidos, acrescentados ou modificados |
| Função no dispositivo | `GV04` | Decorativa / programática / normativa / ritual |
| Vínculo com personagem histórica real | `GV05` | Sim (identificar) / Não — **se sim, o item vai para Comparador** |

---

### Repertório: Continentes (Bloco G-C)

Aplicar quando `B02 = Continentes`

| Campo | Código | Instrução |
|---|---|---|
| Continente representado | `GC01` | Europa / Ásia / África / América / Oceania |
| Hierarquia visual no conjunto | `GC02` | Posição relativa a outros continentes na composição (central / lateral / inferior) |
| Marcadores raciais codificados | `GC03` | Pele, cabelo, vestimenta, fauna associada — descrição detalhada |
| Fauna e flora associadas | `GC04` | Lista dos elementos naturais presentes |
| Relação com colonialismo | `GC05` | A figura encena subordinação, autonomia, exotismo ou neutralidade? |
| Dimensão de gênero | `GC06` | A alegoria reforça ou subverte a gramática de gênero do repertório europeu? |

---

### Repertório: Oceanos e Rios (Bloco G-O)

Aplicar quando `B02 = Oceanos-Rios`

| Campo | Código | Instrução |
|---|---|---|
| Corpo d'água representado | `GO01` | Nome do oceano, mar ou rio; ou "alegórico genérico" |
| Gênero da figura | `GO02` | Feminino / Masculino / Neutro (os rios admitem ambos na tradição) |
| Atributos aquáticos | `GO03` | Urna / tridente / âncora / peixes / juncos / barco — listar |
| Função no contexto jurídico-estatal | `GO04` | Soberania territorial / fronteira / riqueza nacional / outro |
| Associação com projeto civilizatório | `GO05` | A figura evoca exploração, progresso, natureza domesticada? |

---

## Regras de Confiabilidade

- Todo piloto deve ser codificado por **dois codificadores independentes**
- Índice mínimo aceitável: **Kappa de Cohen ≥ 0,70**
- Campos qualitativos (F01–F05): codificação por categorias emergentes com descritor aberto
- Discordâncias nos Blocos B e C são discutidas em reunião e resolvidas por consenso antes do freeze
- Campos do Bloco F permanecem em branco até o freeze

---

## Changelog

| Versão | Data | Mudança |
|---|---|---|
| v0 | mai/2026 | Rascunho inicial com Blocos A–C |
| v1 | jun/2026 | Adição Blocos D–F; campos diferenciados G-V, G-C, G-O; regras de confiabilidade |

---

*Próxima versão após piloto de 10 itens. Qualquer alteração de indicador gera v1.1 com changelog obrigatório.*
