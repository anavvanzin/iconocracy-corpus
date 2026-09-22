# Comparador Genealógico — pré-1800

**Status: fora do pipeline canônico.** Estes registros NÃO entram em
`data/processed/records.jsonl` nem em `corpus/corpus-data.json` — o período de
inclusão do corpus-core é 1800–2000 (`CLAUDE.md` §Corpus Parameters). Este
diretório abriga o **material de comparador genealógico** da Camada 1 do plano
[`docs/PLANO-ALEGORIAS-VIRTUDES-CONTINENTES-OCEANOS.md`](../../docs/PLANO-ALEGORIAS-VIRTUDES-CONTINENTES-OCEANOS.md):
a gramática visual (Virtudes / Iconologia / Emblemata) de que a iconocracia
moderna extrai vocabulários, posições e hierarquias.

## Proveniência

Recuperados da linhagem divergente (nunca propagada à `main`) durante a
auditoria de integridade de 2026-07-01 — ver PR #123, que recuperou os 2 itens
*em período* (Portinari 1948, Visconti 1903) para o corpus-core e reencaminhou
estes 15 para cá. Formato: master-record v1.0, todos schema-válidos
(`validate_schemas.py comparador-pre1800.jsonl --schema master-record` → 15/15 ✓).

## Conteúdo (15 registros)

| # | Obra | Data | Fonte |
|---|------|------|-------|
| 1 | Alciato, *Emblematum liber* — Augsburg (1.ª ed.) | 1531 | Glasgow (emblems.arts.gla.ac.uk) |
| 2 | Loscher, *Allegorie der irdischen und göttlichen Gerechtigkeit* | 1536 | SMB museum-digital |
| 3 | Alciato, *Emblemata* — Lyon (Rovilius) | 1550 | MDZ |
| 4 | *Iustitia* (série *The Virtues*) | ca. 1575–1625 | V&A |
| 5 | Alciato, *Omnia Emblemata* — Antuérpia (Plantin) | 1577 | MDZ |
| 6 | Camerarius, *Symbolorum & emblematum… centuria tertia* | 1596 | MDZ |
| 7 | Ripa, *Iconologia* — Roma 1603 (Heidelberg) ⚠ par duplicado | 1603 | Heidelberg digi |
| 8 | Ripa, *Iconologia* — Roma 1603 (Heidelberg) ⚠ par duplicado | 1603 | Heidelberg digi |
| 9 | Ripa, *Iconologia* — Roma 1603 (MDZ) | 1603 | MDZ |
| 10 | Ripa, *Iconologia* — Siena 1613 (Bd. 1) | 1613 | Heidelberg digi |
| 11 | Saavedra, *Idea de un príncipe político christiano* | 1643 | archive.org |
| 12 | Ripa, *Erneuerte Iconologia oder Bilder-Sprach* — Frankfurt | 1669 | Heidelberg digi |
| 13 | *Justitia* (Holanda) | ca. 1600–1699 | SMK (KKSgb4863) |
| 14 | *Justitia* (Dinamarca) | ca. 1780–1800 | SMK (KKSgb4097) |
| 15 | *Udkast til Retfærdighedsrelieffet på Frihedsstøtten* ⚠ figura masculina | ca. 1792–97 | SMK (KKSgb4255) |

## Flags de curadoria (verificação 2026-07-01)

- **Par duplicado (#7/#8):** dois registros da linhagem apontam para a mesma
  digitalização Heidelberg (`diglit/ripa1603`), atribuídos a DE e IT.
  Preservados verbatim; unificar na curadoria das fichas.
- **Figura masculina (#15):** imagem verificada (SMK IIIF) mostra gênio/putto
  **masculino** alado — fora do critério de gênero mesmo ignorando o período.
  Mantido no dossiê pelo valor genealógico (relevo da Justiça na
  Frihedsstøtten), com este flag.
- **#13 e #14 verificados visualmente** (SMK IIIF): Iustitia feminina com
  balança/espada/venda — comparadores fortes para a genealogia da Iustitia.

## Próximos passos (Camada 1 do plano)

1. Ficha bibliográfica anotada por obra (produto esperado da Camada 1).
2. Entrada no codebook com atributos iconográficos de cada repertório.
3. Unificar o par duplicado Ripa 1603.
4. Decidir campo/flag para uso analítico (ex. `#comparador-genealogico` no
   vault) sem contaminar o N do corpus-core.
