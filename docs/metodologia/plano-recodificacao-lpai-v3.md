# Plano de recodificação do corpus — LPAI v3

Da situação atual (328 registros, 106 dos quais não codificados, instrumento
unidimensional por artefato) até um corpus inteiramente recodificado sob
instrumento estratificado, com confiabilidade declarada e auditável.

Horizonte: julho de 2026 → novembro de 2027
Capacidade declarada: 5 a 8 horas semanais
Configuração de codificação: codificadora única + proxy Kimi K3 como contraste +
Google Cloud Vision como canal independente; vaga de codificador humano B
reservada na arquitetura para uso futuro
Método de revisão: ancorada, com amostra-controle cega

---

## 1. O que o plano resolve

Três problemas, em ordem de gravidade.

O corpus não tem 328 registros codificados — tem 222, e 106 linhas de zeros de
importação que se comportam como medições. Esse bloco fabricou a aparência de
unidimensionalidade do instrumento e inverteu o sinal do regime militar, que
concentra 59,3% de não codificação.

O instrumento mistura, numa única escala ordinal, propriedade material do
suporte, fato institucional e juízo iconográfico. A matriz de correlação já
denuncia a mistura: monocromatização é ortogonal a tudo (r entre 0,07 e 0,27,
e −0,04 com inscrição estatal).

E não há evidência visual disponível para codificar: 90% dos registros apontam
para páginas de acervo, não para arquivos de imagem. Sem bytes em disco não há
Estrato III, e sem Estrato III não há tese.

---

## 2. A ideia que muda o custo do trabalho

Sem codificador humano B, a confiabilidade parece um problema insolúvel. Ela não
é — porque **a estratificação redistribui o ônus da prova de modo que apenas um
estrato precisa de concordância humana.**

| Estrato | Como se estabelece a confiabilidade | Precisa de codificador B? |
|---|---|---|
| I — propriedade material | **medição programática** sobre o arquivo de imagem: número de matizes distintos, saturação média, entropia cromática; serialidade técnica lida dos metadados de catálogo | Não. Reprodutível por execução de script |
| II — fato institucional | **triangulação documental**: decreto, ata, catálogo de emissão. Verificável por terceiros na fonte citada | Não. Verificabilidade substitui concordância |
| III — juízo iconográfico | teste-reteste cego intracodificadora + contraste com proxy K3 + Vision como terceiro canal | Sim, idealmente — e é aqui que a vaga futura entra |

O efeito prático é grande: de dez atributos que exigiriam dupla codificação
humana, sobram oito, e apenas numa amostra estratificada. Monocromatização deixa
de ser juízo e passa a ser número calculado do pixel; serialidade técnica deixa de
ser juízo e passa a ser fato de catálogo. O que era impossível sozinha passa a ser
uma tarefa de sábado.

Há uma consequência epistêmica que vale registrar no apêndice metodológico:
medir monocromatização por script é mais honesto que codificá-la a olho, porque
torna explícito que ela nunca foi um juízo iconográfico. A tese ganha um argumento
onde antes tinha uma inconsistência.

---

## 3. Fases

### Fase 0 — Camada de captação de imagens (em execução)

`tools/scripts/harvest_corpus_images.py` resolve cada `input_url` até um arquivo
de imagem, preferindo IIIF e APIs oficiais antes de qualquer heurística de HTML,
e registra proveniência auditável: URL de origem, estratégia de resolução,
manifesto IIIF, direitos declarados, dimensões, hash e data.

Resolvedores implementados por acervo: Gallica/BnF via manifesto IIIF; Library of
Congress via API de item com escolha da maior derivação; Wikimedia Commons via
`imageinfo` com licença; V&A via API e convenção IIIF do museu; Europeana por
redirecionamento ao ark de origem; genérico com descoberta de manifesto IIIF,
`og:image` e JSON-LD, nessa ordem de preferência.

Duas descobertas operacionais da primeira execução: `loc.gov` devolve 403 para
User-Agent que contenha URL, o que exigiu identificação curta e fallback; e
Numista bloqueia acesso por script (403 em todos os 57 registros), o que precisa
de uma das três saídas abaixo.

**Decisão pendente sobre os 57 registros da Numista:**
1. chave de API da Numista (gratuita para membros) — o script já tem o resolvedor
   pronto, ativado por `NUMISTA_API_KEY`;
2. captação pela sessão de navegador autenticada, item por item;
3. substituição por espelhos em Wikimedia Commons e catálogos nacionais de casa
   da moeda, quando existirem — o que melhora a proveniência, já que Numista é
   agregador e não acervo institucional.

Recomendo a terceira como preferência e a primeira como atalho. Os 15 registros
com URL `iconocracy.corpus` são placeholders sem acervo de origem e precisam de
reprospecção — entram na campanha SCOUT.

**Critério de conclusão:** cada registro tem imagem em cache com resolução
declarada, ou um status de falha tipado que explica por quê. Nenhum registro em
silêncio.

### Fase 1 — Codebook v3 (agosto de 2026)

Redigir o instrumento estratificado, com três blocos de decisão.

**Estratificação.** Estrato I: monocromatização (medida), serialidade técnica.
Estrato II: inscrição estatal, regime de emissão como fato de contexto, recusas
com ato documentado. Estrato III: desincorporação, rigidez postural,
dessexualização desdobrada, uniformização facial, heraldização, enquadramento
arquitetônico, apagamento narrativo, serialidade figural.

**Política de ausência em três estados.** Valor ordinal com frase justificativa;
`NC:<causa>` tipada; `NÃO_CODIFICADO` como estado de proveniência. Zero passa a
significar exclusivamente ausência observada — e ausência observada é dado
positivo, o material das Recusas.

**Limiar de atributo presente, explicitado e justificado.** Hoje é uma constante
em `lpai_indicators.py` que eu escrevi sem que fosse decisão sua. Passar de ≥2
para ≥3 esvazia 70% do corpus; passar para ≥1 quase dobra o inventário médio.
Nenhuma escolha sobre quais atributos entram produz variação dessa magnitude.

**Desdobramentos.** Dessexualização em três observáveis — nudez ou seminudez
classicizante; adereço de cabeça diagnóstico (coroa mural, frígio, diadema,
elmo); objeto empunhado diagnóstico (balança, espada, ramo, bandeira, livro).
Serialidade em técnica e figural.

**Campos reservados para o codificador B futuro:** `coder_id`, `blind`,
`session_id`, `adjudicated_by`. Criar agora custa nada; criar depois exige
migração de 328 registros.

### Fase 2 — Calibração e piloto (setembro de 2026)

Trinta itens, equilibrados por regime, país e suporte, codificados às cegas por
você. O objetivo não é medir nada ainda — é descobrir onde o instrumento novo é
ambíguo, cronometrar o tempo real por item e fixar as regras de decisão para as
armadilhas conhecidas (Justitia/Aequitas, Libertas/Marianne).

Em paralelo, o proxy K3 codifica os mesmos trinta. A discordância é o produto
desta fase: cada item em que máquina e humana divergem aponta um lugar onde a
regra de decisão está subespecificada. Não é medida de qualidade do modelo — é
detector de ambiguidade do instrumento.

**Critério de conclusão:** tempo médio por item conhecido; regras de decisão
revisadas; menos de cinco itens com dúvida irresolúvel.

### Fase 3 — Recodificação em ondas (outubro de 2026 a fevereiro de 2027)

Ordem das ondas por necessidade argumentativa, não por conveniência:

| Onda | Recorte | Registros | Por quê primeiro |
|---|---|---|---|
| 1 | regime militar | 54 | 59,3% não codificados; a afirmação sobre o regime está suspensa até isso |
| 2 | Brasil | 68 | caso central da tese, 42,6% não codificados |
| 3 | Itália e Bélgica | 30 | 50% e 40% não codificados; o volume Brasil–Itália depende deles |
| 4 | França | 90 | maior bloco, melhor cobertura atual (24,4%) |
| 5 | restante | 86 | EUA, Reino Unido, Alemanha, Países Baixos, Portugal, Espanha |

A 8 minutos por item nos itens já codificados (revisão ancorada) e 15 minutos nos
não codificados, o total fica em torno de 60 horas — dez semanas a 6 horas. Com
folga para retrabalho, cinco meses.

**A amostra-controle cega.** A revisão ancorada é mais rápida e herda viés de
ancoragem: você tenderá a confirmar o que já estava lá. Quarenta itens — 12% do
corpus, estratificados — devem ser recodificados **sem ver** a codificação
anterior. A comparação entre a taxa de mudança na amostra cega e na amostra
ancorada estima o efeito de ancoragem, que passa a ser um número declarado na
tese em vez de uma objeção de banca. Custo: dez horas. É o melhor seguro
metodológico disponível por esse preço.

### Fase 4 — Confiabilidade (março a maio de 2027)

Três protocolos, um por estrato.

**Estrato I:** rodar a medição programática duas vezes, em versões diferentes do
script, e verificar identidade dos resultados. Reprodutibilidade, não
concordância.

**Estrato II:** auditoria de fontes por amostragem — 30 itens, verificar se a
fonte citada existe e sustenta o fato codificado. É a auditoria de citações
aplicada ao corpus.

**Estrato III:** teste-reteste cego, no mínimo oito semanas após a codificação
original, em amostra estratificada de 50 itens. Reportar kappa por atributo e —
mais importante — o relato qualitativo dos desacordos: quais atributos são
instáveis e por quê. Atributo que não estabiliza entre duas leituras suas próprias
não sobrevive a uma banca, e deve ser redefinido ou aposentado.

Nesta fase, se houver codificador humano B disponível, ele entra sobre a mesma
amostra de 50 itens e a arquitetura já o acomoda sem migração.

### Fase 5 — Reconstrução do atlas (junho a agosto de 2027)

Os oito painéis reescritos sobre o corpus recodificado, com taxa de codificação
declarada por célula. O painel ENDURECIMENTO em particular: a afirmação de
acúmulo de atributos precisa ser refeita sobre dados que não são artefato de
cobertura, e a inflexão militar precisa ser reavaliada ou abandonada.

### Fase 6 — Folga (setembro a novembro de 2027)

Deliberadamente vazia. Três meses de reserva antes do prazo. Se as fases
anteriores escorregarem — e escorregam —, é aqui que o atraso é absorvido, e não
na qualidade da codificação.

---

## 4. Calendário

| Período | Fase | Entregável |
|---|---|---|
| jul–ago 2026 | 0 | corpus com imagem em cache e proveniência; decisão sobre Numista |
| ago 2026 | 1 | codebook v3 publicado, política de ausência registrada, limiar justificado |
| set 2026 | 2 | piloto de 30 itens, regras de decisão revisadas, tempo real por item |
| out 2026–fev 2027 | 3 | 328 registros recodificados; amostra-controle cega medida |
| mar–mai 2027 | 4 | relatório de confiabilidade por estrato |
| jun–ago 2027 | 5 | oito painéis do atlas reconstruídos |
| set–nov 2027 | 6 | folga |

A escrita da tese corre em paralelo, não depois. A Fase 3 produz material de
painel continuamente; cada onda concluída libera um recorte para escrita.

---

## 5. O que muda no repositório

**Imediato:**
- `docs/decisions/` — decisão sobre a conversão dos 106 zeros em `NÃO_CODIFICADO`,
  preservando o valor original em campo de proveniência;
- `schema/codebook-v3.0.0.md` — instrumento estratificado;
- `tools/schemas/` — três estados por indicador, campos de codificador reservados;
- `tools/scripts/lpai_indicators.py` — contagem de atributos **por estrato**, não
  global. A contagem global que eu instituí soma incomensuráveis: é menos falsa
  que a média, mas não é inocente;
- `tools/scripts/measure_stratum_i.py` (novo) — medição colorimétrica de
  monocromatização a partir do arquivo de imagem.

**Durante a Fase 3:**
- fila de recodificação em staging, com `coder_id` e `blind` por sessão;
- o proxy K3 rodando sobre cada onda, para contraste;
- health check semanal reportando taxa de codificação por regime e país — a
  métrica que faltava.

---

## 6. Riscos

**A resolução das imagens pode não sustentar o Estrato III.** Uma moeda a 400
pixels não permite julgar uniformização facial. O relatório de captação classifica
cada imagem por faixa de resolução, e atributos não verificáveis na resolução
disponível devem receber `NC:resolucao_inadequada` — não um palpite. Se a
proporção de imagens insuficientes for alta, parte do Estrato III precisa ser
repensada, e é melhor descobrir isso em agosto de 2026 do que em 2027.

**A revisão ancorada pode apenas reproduzir o corpus antigo.** Mitigado pela
amostra-controle cega, mas o risco não desaparece: se a taxa de mudança na amostra
cega for muito superior à da ancorada, a decisão honesta é recodificar tudo às
cegas — o que cabe no calendário, consumindo a folga da Fase 6.

**A codificação solo tem um teto de credibilidade.** Teste-reteste mede
estabilidade, não intersubjetividade. Isso deve ser declarado como limitação
explícita, não contornado. A vaga do codificador B fica aberta na arquitetura, e
um único colega do Ius Gentium codificando 50 itens em 2027 converteria a
limitação em resultado.

**Fadiga de codificação.** Cinquenta itens seguidos produzem deriva de critério.
Sessões de no máximo duas horas, e nunca duas ondas diferentes no mesmo dia.

---

## 7. A primeira semana

1. Terminar a captação de imagens e ler o relatório de cobertura por acervo e por
   faixa de resolução.
2. Decidir o caminho da Numista — 57 registros, 17% do corpus.
3. Aprovar a conversão dos 106 zeros em `NÃO_CODIFICADO` e registrá-la como
   decisão.
4. Escrever a política de ausência de três estados e fixar o limiar de atributo.
5. Escolher os 30 itens do piloto.

---

Base empírica: `ARQUITETURA-ATRIBUTOS-LPAI-V3.md` e as análises reprodutíveis
`analise_indicadores.py`, `analise_dimensional.py`, `analise_lacunas.py`,
`analise_evidencia.py`. Base bibliográfica:
`pesquisa-arquitetura-atributos.md`.
