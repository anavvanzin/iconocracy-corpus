# Compilação da tese ICONOCRACIA

A fonte canônica da tese é `tese/manuscrito/`, na raiz do repositório.
Este diretório reúne o Makefile, `references.bib`, `abnt.csl`, `metadata.yaml`
e `template.docx`. Os capítulos Markdown aqui são espelhos para Obsidian;
a tese completa e os capítulos individuais compilam as fontes canônicas.

Na raiz do repositório:

```sh
make -C vault/tese docx
make -C vault/tese pdf
make -C vault/tese capitulo-4.docx
make -C vault/tese capitulo-4.pdf
make -C vault/tese clean
```

`make -C vault/tese` também compila o DOCX. `references.bib` é obrigatório
em todos os alvos de compilação. Pandoc com citeproc e o template versionado
são necessários; o PDF usa LuaLaTeX e TeX Gyre Termes por padrão, com instalação
TeX Live completa e fontes disponíveis. Em ambientes com outro mecanismo:

```sh
make -C vault/tese pdf PDF_ENGINE=xelatex PDF_FONT='DejaVu Serif'
```

Os resultados ficam em `vault/tese/output/`; os alvos completos também copiam
as saídas para `tese/tese_completa.docx` e `tese/tese_completa.pdf`.
`clean` remove apenas `output/`, preservando essas cópias. O DOCX em `tese/`
ainda é versionado: não incluir sua alteração binária acidentalmente após
uma validação. O PDF compilado deixou de ser versionado na PR #239 e está
ignorado pelo Git; deve ser regenerado antes de distribuir. Não é fonte
canônica, e as compilações históricas em diretórios datados são preservadas.

O Makefile antigo de `tese/manuscrito/` foi removido na PR #239 porque
listava capítulos inexistentes e não era usado pelos comandos documentados.
Não recriar esse segundo caminho. O observador `scripts/watch-compile.py`
(e sua cópia em `tools/scripts/`) acompanha `tese/manuscrito/` e invoca o
Makefile deste diretório. O serviço Docker `thesis` monta o repositório
inteiro para preservar os caminhos relativos das fontes.

## Numeração e referências

A numeração editorial está nos títulos Markdown, inclusive `I.x` na
introdução e `C.x` na conclusão. Pandoc não acrescenta `--number-sections`:
isso evita duplicar números e contar a introdução como Capítulo 1. O
Capítulo 4 usa `4.1`–`4.8` e `4.5.1`–`4.5.4`; suas remissões locais foram
atualizadas. Não renumerar capítulos por posição na lista de entradas.

O sumário mantém os níveis de títulos existentes (profundidade 3). O
`nocite: '@*'` de `metadata.yaml` inclui todas as entradas da bibliografia,
pois o manuscrito também usa citações autor-data em prosa. Sucesso do
citeproc não equivale a conferir a correspondência de cada citação em
prosa com o BibTeX; essa revisão acadêmica continua separada.

## Verificações

```sh
python -m pytest tests/test_thesis_build.py tests/test_abnt_online.py -q
python tools/scripts/validate_schemas.py
```

As regressões de build compilam cópias temporárias e verificam numeração,
fontes canônicas, alvo padrão e bloqueio de bibliografia ausente. A suíte
ABNT verifica URL e data de acesso sem alterar as referências.
