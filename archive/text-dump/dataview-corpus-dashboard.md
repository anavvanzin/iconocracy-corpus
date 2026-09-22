---
tags: [tipo/dashboard, status/permanente]
---

# Corpus Dashboard — Dataview Queries

> Copiar este arquivo para o vault. Requer o plugin **Dataview** instalado e habilitado.
> As queries abaixo assumem que as notas SCOUT-XXX estão em `01-corpus/candidatos/`
> com frontmatter padronizado (id, pais, suporte, regime, endurecimento, confianca, status).

---

## 1. Visão geral do corpus

```dataview
TABLE WITHOUT ID
  length(rows) AS "Total",
  length(filter(rows, (r) => r.status = "candidato")) AS "Candidatos",
  length(filter(rows, (r) => r.status = "confirmado")) AS "Confirmados",
  length(filter(rows, (r) => r.status = "excluido")) AS "Excluídos"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
FLATTEN "corpus" AS group_key
GROUP BY group_key
```

---

## 2. Distribuição por país

```dataview
TABLE WITHOUT ID
  pais AS "País",
  length(rows) AS "Itens",
  round(length(rows) / 250 * 100) + "%" AS "Meta (250)"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY pais
SORT length(rows) DESC
```

---

## 3. Distribuição por suporte

```dataview
TABLE WITHOUT ID
  suporte AS "Suporte",
  length(rows) AS "Itens"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY suporte
SORT length(rows) DESC
```

---

## 4. Distribuição por regime iconocrático

```dataview
TABLE WITHOUT ID
  regime AS "Regime",
  length(rows) AS "Itens",
  round(length(filter(rows, (r) => r.endurecimento = "ALTO")) / length(rows) * 100) + "%" AS "% Endurec. ALTO"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY regime
SORT length(rows) DESC
```

---

## 5. Grau de endurecimento

```dataview
TABLE WITHOUT ID
  endurecimento AS "Endurecimento",
  length(rows) AS "Itens"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY endurecimento
SORT choice(endurecimento = "ALTO", 1, choice(endurecimento = "MÉDIO", 2, 3)) ASC
```

---

## 6. Confiança da análise visual

```dataview
TABLE WITHOUT ID
  confianca AS "Confiança",
  length(rows) AS "Itens"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY confianca
```

---

## 7. Lacunas de cobertura — País × Regime

> Identifica combinações com menos de 5 itens.

```dataview
TABLE WITHOUT ID
  pais + " × " + regime AS "Combinação",
  length(rows) AS "Itens",
  choice(length(rows) < 5, "⚠️ LACUNA", "✓") AS "Status"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY pais + "|" + regime
SORT length(rows) ASC
```

---

## 8. Itens com flags pendentes (#verificar)

```dataview
TABLE WITHOUT ID
  id AS "ID",
  titulo AS "Título",
  pais AS "País",
  file.tags AS "Flags"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato" AND (
  contains(file.tags, "#verificar") OR
  contains(file.tags, "#verificar-data") OR
  contains(file.tags, "#verificar-autoria") OR
  contains(file.tags, "#verificar-imagem") OR
  contains(file.tags, "#sem-iiif") OR
  contains(file.tags, "#possivel-duplicata")
)
SORT pais ASC, id ASC
```

---

## 9. Cronologia das sessões Scout

```dataview
TABLE WITHOUT ID
  id AS "Sessão",
  data AS "Data",
  total_candidatos AS "Candidatos",
  paises AS "Países",
  query_executada AS "Query"
FROM "01-corpus/sessoes"
WHERE tipo = "sessao-scout"
SORT data DESC
LIMIT 20
```

---

## 10. Últimas adições ao corpus

```dataview
TABLE WITHOUT ID
  id AS "ID",
  titulo AS "Título",
  pais AS "País",
  suporte AS "Suporte",
  regime AS "Regime",
  data_scout AS "Adicionado em"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
SORT data_scout DESC
LIMIT 15
```

---

## 11. País × Suporte (matriz de cobertura)

```dataview
TABLE WITHOUT ID
  pais AS "País",
  length(filter(rows, (r) => r.suporte = "moeda")) AS "Moeda",
  length(filter(rows, (r) => r.suporte = "selo")) AS "Selo",
  length(filter(rows, (r) => r.suporte = "monumento")) AS "Monum.",
  length(filter(rows, (r) => r.suporte = "estampa")) AS "Estampa",
  length(filter(rows, (r) => r.suporte = "frontispicio")) AS "Front.",
  length(filter(rows, (r) => r.suporte = "papel-moeda")) AS "Papel-m.",
  length(filter(rows, (r) => r.suporte = "cartaz")) AS "Cartaz"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY pais
SORT pais ASC
```

---

## 12. Motivos alegóricos mais frequentes

```dataview
TABLE WITHOUT ID
  motivo_alegorico AS "Motivo",
  length(rows) AS "Itens",
  join(distinct(rows.pais), ", ") AS "Países"
FROM "01-corpus/candidatos"
WHERE tipo = "corpus-candidato"
GROUP BY motivo_alegorico
SORT length(rows) DESC
```

---

## Notas de uso

- **Atualização:** As queries rodam ao vivo sobre os arquivos no vault. Não precisa de sync manual.
- **Paths:** Se você ainda usa a estrutura antiga (`vault/candidatos/`), substitua `"01-corpus/candidatos"` por `"candidatos"` nas queries.
- **Performance:** Com 250+ notas, Dataview pode demorar ~1s. Isso é normal.
- **Combinação:** Use as queries de lacunas (§7 e §11) para guiar as próximas campanhas Scout.
