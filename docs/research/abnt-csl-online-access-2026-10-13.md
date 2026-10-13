# CSL ABNT: referências online — comparação Pandoc/citeproc

## Escopo

Ajuste do estilo `vault/tese/abnt.csl`, separado da revisão bibliográfica da PR #234. Base: `main` em `5839bd057d1f27c75be2a70d90362bd0794a51a8`. As duas fixtures reproduzem as entradas bibliográficas da #234 em `550edfa25093353c6e9636419afc64a1e307ca5e`, incluindo `urldate = {2026-10-06}`. `vault/tese/references.bib` e o texto do capítulo não são alterados.

Os ramos `book` e `article-newspaper article-magazine article-journal` passam a chamar `access`. O separador entre URL e data fica no `group delimiter=". "` da macro: ele só aparece quando ambos os elementos são renderizados. Isso evita um ponto inicial quando existe apenas a data. Os afixos da chamada só são emitidos quando há conteúdo; referências sem ambos os campos conservam a saída anterior, inclusive sua pontuação.

## Reprodução

Pandoc 3.1.3, citeproc integrado, idioma `pt-BR`:

```bash
python -m pytest tests/test_abnt_online.py -q
pandoc tests/fixtures/abnt-online/sample.md --citeproc \
  --csl=vault/tese/abnt.csl \
  --bibliography=tests/fixtures/abnt-online/references.bib \
  --metadata=lang:pt-BR --wrap=none -t plain
```

Para obter o estilo anterior, extraia `vault/tese/abnt.csl` do commit base com `git show 5839bd057d1f27c75be2a70d90362bd0794a51a8:vault/tese/abnt.csl` e repita o comando apontando `--csl` para esse arquivo. Trocar `-t plain` por `-o amostra.docx` compila a mesma amostra em Word.

## Antes

```text
Referências online

AGAMBEN, Giorgio. The Signature of All Things: On Method. Tradução: Luca D’Isanto;Tradução: Kevin Attell. New York: Zone Books, 2009.

MONDZAIN, Marie-José. Qui refuse l’économie refuse l’iconomie. La Voix du Regard, n. 14, p. 14–22, 2001.
```

## Depois

```text
Referências online

AGAMBEN, Giorgio. The Signature of All Things: On Method. Tradução: Luca D’Isanto;Tradução: Kevin Attell. New York: Zone Books, 2009. Disponível em: <https://www.zonebooks.org/books/101-the-signature-of-all-things-on-method>. Acesso em: 6 out. 2026.

MONDZAIN, Marie-José. Qui refuse l’économie refuse l’iconomie. La Voix du Regard, n. 14, p. 14–22, 2001. Disponível em: <https://surlimage.info/ecrits/pdf/mondzain/010000-Economie-Iconomie.pdf>. Acesso em: 6 out. 2026.
```

## Verificações

- Testes antes do ajuste: 13 falhas pela omissão de URL/data; 4 casos sem esses campos passam.
- Testes depois: 17 passam. Matriz: duas entradas × quatro combinações de URL/data × com/sem volume e páginas, mais compilação direta das entradas BibLaTeX.
- `offline.json` registra a saída anterior dos quatro controles sem URL/data. Comparações integrais detectam alterações no corpo ou pontuação, não apenas presença de rótulos.
- Amostra DOCX compilada sem avisos; comparação textual realizada via citeproc.
- Comparação HTML das 97 entradas da bibliografia da #234: todas as 91 sem URL/data permaneceram idênticas. Só cinco entradas mudaram: `ginzburg1989`, `hartman2008`, `fuentes2016`, `agamben2009` e `mondzain2001entretien`; todas pertencem aos ramos ajustados. A referência online do ramo já atendido permaneceu idêntica.
- `validate_schemas.py`: 337/337 registros válidos.
- Workflow dedicado `Thesis CSL` executa os testes quando o estilo, as fixtures ou o teste são modificados; o workflow geral atual não é disparado por esses caminhos.
- Suíte completa `python -m pytest tests/ -q --tb=short`: 485 passam, 2 xfailed, 2 subtestes passam; 8 avisos preexistentes de marca `unit` não registrada em `test_draft_flow.py` e `test_id_crosswalk.py`.
- `git diff --check`: sem erros.
