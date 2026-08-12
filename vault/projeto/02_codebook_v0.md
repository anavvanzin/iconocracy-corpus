# Codebook v0 — Corpus Iconocracia
## Protocolo de Codificação de Alegorias Femininas em Dispositivos Jurídicos e Estatais

**Versão:** 0.1 (junho 2026) — pré-piloto  
**Status:** rascunho para teste; NÃO usar para análise final antes do freeze  
**Changelog:** ver seção 6

---

## 1. Sistema de Identificação

### Formato do ID
```
[PAÍS]-[SUPORTE]-[NÚMERO SEQUENCIAL]
```

### Códigos de país
| Código | País |
|---|---|
| BRA | Brasil |
| FRA | França |
| GBR | Grã-Bretanha |
| ESP | Espanha |
| MEX | México |
| USA | Estados Unidos |

### Códigos de suporte
| Código | Suporte |
|---|---|
| MOE | Moeda |
| SEL | Selo postal |
| HER | Heráldica (brasão / armas) |
| MON | Monumento / escultura |
| ARQ | Arquitetura forense |
| PAR | Paratexto normativo (frontispício, capa de código, etc.) |
| OTR | Outro (especificar) |

**Exemplo:** `BRA-MOE-001` = primeiro item do corpus, moeda, Brasil.

---

## 2. Ficha de Codificação

### Bloco A — Identificação

| Campo | Tipo | Instruções |
|---|---|---|
| **ID** | texto | Sistema acima |
| **País** | lista | Código de país |
| **Suporte** | lista | Código de suporte |
| **Título / denominação** | texto livre | Nome oficial ou descrição descritiva |
| **Data** | texto | Ano ou intervalo; "ca." para aproximado |
| **Instituição emissora** | texto | Casa da Moeda, Correios, tribunal, etc. |
| **Fonte / localização** | texto | Museu, acervo digital, coleção particular |
| **URL / referência** | texto | Link ou referência bibliográfica |
| **Dentro do escopo core?** | sim / não / parcial | Janela 1800–2000 e suporte core |

### Bloco B — Figura Alegórica

| Campo | Tipo | Opções / Instruções |
|---|---|---|
| **Tipo de alegoria** | lista múltipla | Virtude cardinal; Virtude teologal; República/Liberdade; Justiça; Nação; Continente; Oceano/Rio; Outro |
| **Nome da figura** | texto | Ex.: Justitia, Marianne, República, Europa, Atlântico |
| **Identificação certa?** | sim / provável / incerta | Grau de certeza da identificação iconográfica |
| **Atributos visuais** | texto livre | Listar todos: venda, balança, espada, capacete, toga, coroa, etc. |
| **Postura / gesto** | lista | Estática; Em movimento; Triunfante; Submetida; Protetora; Outra |
| **Relação com texto** | lista | Substitui texto; Acompanha texto; Enmoldurada por texto; Independente |

### Bloco C — Marcadores de Gênero, Raça e Corpo

| Campo | Tipo | Opções / Instruções |
|---|---|---|
| **Gênero da figura** | lista | Feminino; Masculino; Andrógino; Indefinido |
| **Codificação racial** | lista | Branca/europeia; Mestiça/indígena; Negra; Ambígua; Não aplicável |
| **Tipo corporal** | lista | Clássico-greco-romano; Medieval; Barroco; Neoclássico; Moderno; Outro |
| **Vestimenta** | texto livre | Toga, drapeado, nudez parcial, roupa contemporânea, etc. |
| **Cabelo / cobertura** | texto livre | Cabelo solto, véu, capacete, coroa cívica, etc. |
| **Seios expostos?** | sim / não | Registrar sempre; relevante para análise de corpo e soberania |
| **Notas de gênero/raça** | texto livre | Observações que não cabem nas listas |

### Bloco D — Circulação e Uso Institucional

| Campo | Tipo | Instruções |
|---|---|---|
| **Alcance de circulação** | lista | Local; Regional; Nacional; Imperial/colonial; Internacional |
| **Função institucional primária** | lista | Legitimação monetária; Comunicação postal; Identidade nacional; Memória jurídica; Protocolo normativo; Outra |
| **Contexto de emissão** | texto livre | Crise, celebração, reforma constitucional, guerra, etc. |
| **Duração em uso** | texto | Datas de emissão e retirada, se conhecidas |
| **Substituída por quê?** | texto livre | Se aplicável: motivo da troca de efígie |

### Bloco E — Conflito de Imagens / Iconoclasmo

| Campo | Tipo | Instruções |
|---|---|---|
| **Houve iconoclasmo?** | sim / não / provável | |
| **Tipo de conflito** | lista | Vandalização; Substituição oficial; Protesto; Apagamento; Resignificação artística; Outro |
| **Data do conflito** | texto | Ano ou intervalo |
| **Agente do conflito** | texto livre | Quem realizou a ação |
| **Documentação** | texto | Fonte que registra o conflito |

### Bloco F — Análise Iconológica (nível interpretativo)

*Preenchimento apenas após piloto e freeze do dataset.*

| Campo | Tipo | Instruções |
|---|---|---|
| **Nível pré-iconográfico** | texto livre | O que se vê: descrição factual da imagem |
| **Nível iconográfico** | texto livre | Identificação dos atributos segundo o repertório (Ripa, etc.) |
| **Nível iconológico** | texto livre | Interpretação: que valores, tensões e ideologias a imagem veicula |
| **Relação com hipótese central** | texto livre | Como o item confirma, complexifica ou contradiz o argumento da tese |

---

## 3. Campos Diferenciados por Repertório

### 3.1 Virtudes (Justiça, Prudência, Fortaleza, Temperança, Veritas, etc.)

| Campo adicional | Instruções |
|---|---|
| **Virtude específica** | Nome; verificar contra Ripa e fontes medievais |
| **Versão da iconologia usada** | Ripa 1593, 1603, edição ilustrada, adaptação local |
| **Contexto arquitetônico** | Se em edifício: local exato (fachada, frontão, sala de audiências, etc.) |
| **Hierarquia no programa iconográfico** | Figura central, lateral, subordinada, em série |

### 3.2 Continentes (Europa, América, Ásia, África)

| Campo adicional | Instruções |
|---|---|
| **Continente representado** | Europa / América / Ásia / África |
| **Hierarquia visual entre continentes** | Posição relativa, tamanho, atributos de poder ou subordinação |
| **Codificação racial da América** | Indígena, mestiça, branca à europeia — registrar a escolha |
| **Contexto geopolítico** | Colonial, imperial, pós-independência |
| **Texto acompanhante** | Legenda, epígrafe, título — transcrever |

### 3.3 Oceanos e Rios

| Campo adicional | Instruções |
|---|---|
| **Corpo d'água representado** | Atlântico, Pacífico, Amazonas, Tejo, etc. |
| **Gênero da personificação** | Feminino / masculino — e por quê (se discernível) |
| **Articulação com soberania territorial** | Como a imagem conecta o corpo d'água à nação ou ao império |
| **Suporte específico** | Em moeda, em mapa, em frontispício de tratado, em edifício portuário, etc. |

---

## 4. Regras de Confiabilidade

- Todos os campos dos Blocos A–E devem ser codificados por **dois pesquisadores independentes** antes do freeze.
- Cálculo de **Kappa de Cohen** para campos categóricos; taxa de concordância simples para campos de texto.
- Limiar mínimo de confiabilidade: **κ ≥ 0.70** para todos os campos fechados dos Blocos B e C.
- Discordâncias resolvidas por consenso ou por terceiro codificador.
- **Bloco F** (análise iconológica): apenas após freeze e apenas pela pesquisadora principal.

---

## 5. Pipeline Obrigatório

```
Teoria → Codebook → Amostragem → Piloto (10 itens) → 
Cálculo de κ → Revisão do codebook → Novo piloto se necessário → 
Freeze do dataset → Codificação completa → Análise
```

**Proibido:** inferências interpretativas antes do freeze.  
**Proibido:** mudança de indicador sem nova versão e changelog.

---

## 6. Changelog

| Versão | Data | Alteração |
|---|---|---|
| 0.1 | jun. 2026 | Criação. Campos básicos + diferenciados para Virtudes, Continentes, Oceanos |

---

*Codebook v0 — pré-piloto. Próxima versão após piloto de 10 itens.*
