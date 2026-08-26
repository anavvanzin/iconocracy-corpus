# Codebook — 10 Indicadores Ordinais de Purificação

> **Status 2026-04-24:** este codebook permanece como referencia operacional
> dos 10 indicadores, mas esta subordinado a
> `docs/methodology/lpai-v2-as-capta.md`. O indice composto e capta
> interpretativa: serve para selecao, ordenacao, filtros e auditoria, nao como
> prova isolada do regime iconocratico.

Este codebook descreve os 10 indicadores usados para medir o grau de
**purificação simbólica** das alegorias femininas no corpus Iconocracia.

Cada indicador é medido em escala ordinal de **0 a 3**:

| Valor | Significado |
|-------|-------------|
| 0 | Ausente |
| 1 | Fraco / vestigial |
| 2 | Moderado / parcial |
| 3 | Forte / dominante |

---

## Indicadores

### 1. `desincorporacao` — Desincorporação do corpo feminino

Grau em que a figura feminina perde traços corporais concretos (carnalidade,
sensualidade, marcas étnicas) e se torna forma abstrata ou geométrica.

- **0:** Corpo naturalista, carnal, individualizado
- **1:** Corpo idealizado mas ainda orgânico
- **2:** Corpo estilizado, traços genéricos
- **3:** Forma puramente geométrica ou ausência de corpo

### 2. `rigidez_postural` — Rigidez postural e hierática

Grau de rigidez, frontalidade e imobilidade da figura.

- **0:** Movimento dinâmico, gesto espontâneo
- **1:** Pose contida mas com algum movimento
- **2:** Postura rígida, frontal, simétrica
- **3:** Hieratismo total, imobilidade estatuária

### 3. `dessexualizacao` — Dessexualização

Grau de supressão de marcadores de sexualidade e erotismo.

- **0:** Nudez ou erotismo explícito
- **1:** Decote ou formas corporais sugeridas
- **2:** Corpo coberto mas feminilidade visível
- **3:** Gênero indeterminado ou completamente encoberto

### 4. `uniformizacao_facial` — Uniformização facial

Grau em que o rosto perde traços individuais e se torna máscara tipificada.

- **0:** Retrato individualizado, expressão viva
- **1:** Rosto idealizado mas expressivo
- **2:** Rosto genérico, expressão neutra
- **3:** Sem rosto ou máscara pura

### 5. `heraldizacao` — Heraldização dos atributos

Grau em que atributos (balança, espada, barrete, fasces) se tornam signos
heráldicos autônomos, descolados do corpo.

- **0:** Atributos integrados à ação da figura
- **1:** Atributos portados mas estáticos
- **2:** Atributos destacados, quase autônomos
- **3:** Atributos isolados como emblemas (sem corpo)

### 6. `enquadramento_arquitetonico` — Enquadramento arquitetônico

Grau em que a figura é absorvida por moldura arquitetônica (frontão,
nicho, medalhão, selo).

- **0:** Figura em espaço aberto/narrativo
- **1:** Fundo arquitetônico discreto
- **2:** Moldura arquitetônica define a composição
- **3:** Figura reduzida a elemento decorativo de edifício/selo

### 7. `apagamento_narrativo` — Apagamento da narrativa

Grau de supressão do contexto narrativo (cena, ação, outros personagens).

- **0:** Cena narrativa completa com interação
- **1:** Narrativa sugerida, poucos personagens
- **2:** Figura isolada com vestígio de contexto
- **3:** Figura completamente isolada, fundo neutro

### 8. `monocromatizacao` — Monocromatização / redução cromática

Grau de redução da paleta de cores em direção ao monocromático.

- **0:** Policromia rica, cores naturalistas
- **1:** Paleta reduzida mas ainda colorida
- **2:** Bicromia ou tons muito restritos
- **3:** Monocromático / preto-e-branco / dourado-e-branco

### 9. `serialidade` — Serialidade e repetição

Grau em que a imagem é reproduzida em série (selos, moedas, cédulas,
cartazes) com variação mínima.

- **0:** Obra única (pintura, escultura singular)
- **1:** Tiragem limitada (gravura, litografia)
- **2:** Reprodução em média escala (cartaz, livro)
- **3:** Reprodução massiva (selo, moeda, cédula, bandeira)

### 10. `inscricao_estatal` — Inscrição em dispositivo estatal

Grau de vinculação direta a aparato jurídico-estatal (brasão, selo oficial,
fachada de tribunal, cédula de banco central).

- **0:** Obra autônoma sem vínculo estatal
- **1:** Encomenda oficial mas sem insígnia
- **2:** Contém insígnia estatal como elemento
- **3:** É o próprio dispositivo estatal (selo, brasão, moeda)

---

## Índice Composto

O **índice de purificação** é a média aritmética dos 10 indicadores (0–3),
podendo ser reportado como valor contínuo (0.0–3.0) ou convertido para
percentual (0–100%).

```
purificacao = mean(desincorporacao, rigidez_postural, dessexualizacao,
                   uniformizacao_facial, heraldizacao, enquadramento_arquitetonico,
                   apagamento_narrativo, monocromatizacao, serialidade,
                   inscricao_estatal)
```

## Uso nos Notebooks

- `01_exploratory.ipynb` — distribuição dos indicadores (Cap. 6.1)
- `02_kruskal_wallis.ipynb` — regimes × morfologia (Cap. 6.2)
- `03_regression.ipynb` — preditores do endurecimento (Cap. 6.3)
- `04_correspondence.ipynb` — circulação transatlântica (Cap. 6.4)
