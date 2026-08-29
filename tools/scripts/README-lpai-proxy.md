# Codificador-proxy LPAI

Guia operacional de `tools/scripts/lpai_proxy_coder_k3.py`.

## Escopo

O script aplica o instrumento LPAI a registros do corpus como
**codificador-proxy**. Sua saída é uma proposta situada (*capta*), sem
autoridade humana. Ela não substitui codificação ou adjudicação humana e não
promove dados ao corpus.

O prompt operacional tem uma única fonte:
`docs/methodology/codebooks/codebook-MASTER.md`, seção 16. O Python lê essa
seção em tempo de execução; não mantém uma cópia do prompt.

O script não calcula nem emite `purificacao_composto`, média ou outro escore
agregado. Os dez indicadores ordinais e o inventário verbal permanecem
indícios para leitura qualitativa.

## Instalação

A partir da raiz do repositório:

```bash
conda env create -f environment.yml
conda activate iconocracy
```

Em ambiente sem Conda, instale ao menos as dependências declaradas em
`requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Versões

Consulte a versão do programa:

```bash
python tools/scripts/lpai_proxy_coder_k3.py --version
```

Essa é a versão do **script**, registrada em `script_version`. Ela é distinta
de:

- `proxy_schema_version`, versão do contrato do envelope JSONL;
- `codebook_version`, lida do front matter do codebook;
- `prompt_version`, versão do envelope/instruções de proxy;
- `model`, identificador do modelo chamado.

## Variáveis de ambiente

Uma execução real requer:

```bash
export MOONSHOT_API_KEY="..."
```

Não registre a chave em arquivos do repositório. `--dry-run` não requer chave,
não cria cliente e não toca a rede.

## Dry-run

Valide caminho, instrumento, seleção e disponibilidade local de evidência:

```bash
python tools/scripts/lpai_proxy_coder_k3.py --all --dry-run --limit 3
```

Para IDs específicos:

```bash
python tools/scripts/lpai_proxy_coder_k3.py \
  --items UUID-1,UUID-2 \
  --dry-run
```

O `item_id` esperado é o UUID de `data/processed/records.jsonl`, não o ID
público de `corpus/corpus-data.json`.

## Execução

Exemplo limitado:

```bash
python tools/scripts/lpai_proxy_coder_k3.py --all --limit 40
```

Com imagens locais nomeadas por `<item_id>.<ext>`:

```bash
python tools/scripts/lpai_proxy_coder_k3.py \
  --all \
  --limit 40 \
  --images-dir /caminho/para/imagens
```

Sem `--images-dir`, o script tenta obter apenas URLs públicas HTTP(S). Cada
download é feito em streaming, com limite fixo de 10 MiB, redirects validados,
`Content-Type` de imagem e assinatura binária compatível. Localhost, endereços
privados, link-local e reservados são recusados. PDF, HTML — ainda que renomeado
como `.jpg` — e formatos sem assinatura suportada não são enviados ao modelo.
O cliente ignora proxies herdados do ambiente e revalida a resolução DNS no
instante da conexão, fechando mudança de endereço entre checagem e requisição.
Use `--allow-textual` somente quando a codificação sem imagem for
metodologicamente deliberada; itens insuficientes devem sair como não
codificáveis.

## Contexto entregue ao codificador

O conteúdo por item separa explicitamente três proveniências:

1. `ledger.input`: título, data, local e URL de entrada;
2. `purificacao` preexistente: `record_metadata.medium` e `notes`;
3. `webscout`: `summary_evidence`, `gaps` e, quando presentes,
   `search_results`.

Listas, dicionários, profundidade e textos têm limites fixos; cada bloco de
fonte ocupa no máximo 4.000 caracteres. As anotações anteriores são pistas
documentais, não autoridade nem prova de sentido recebido. O prompt lembra
expressamente que recepção histórica exige fonte específica e que o proxy
codifica somente o sentido produzido pelo dispositivo.

## Saída e formato

O destino padrão é:

```text
data/staging/lpai-proxy-k3-schema-v1-runs.jsonl
```

O nome inclui a versão principal do schema para impedir migração ou reescrita
silenciosa de linhas incompatíveis. O antigo
`data/staging/lpai-proxy-k3-runs.jsonl` é **somente histórico**: o default novo
não o lê, valida, altera ou incorpora. Não renomeie o arquivo legado para o
default atual.

Para retomar ou criar outro arquivo compatível com o schema corrente, escolha-o
explicitamente sob `data/staging/`:

```bash
python tools/scripts/lpai_proxy_coder_k3.py \
  --all \
  --output data/staging/lpai-proxy-k3-schema-v1-campanha-a.jsonl
```

O arquivo indicado por `--output` precisa conter exclusivamente envelopes com
`proxy_schema_version: "1.0.0"` válidos contra o schema corrente. Um arquivo
legado sem esse campo falha fechado antes de cliente ou rede; o script não o
migra automaticamente.

Cada linha JSONL é validada contra
`tools/schemas/lpai-proxy-record.schema.json` antes da abertura do arquivo. O
envelope registra, entre outros:

- `proxy_only: true`;
- `authority: "proxy"`;
- `merge_policy: "requires_human_adjudication"`;
- `script_version`, `proxy_schema_version`, `prompt_version` e
  `codebook_version`;
- modelo, data, fonte da imagem e uso reportado pela API;
- `proposta`, com os dez indicadores, inventário verbal e os campos situados do
  §16, incluindo `vetor_colonial`, `atributos_iconograficos`,
  `hipotese_racial`, `programa_id`, `ordem_no_programa`,
  `finalidade_atribuida`, `power_at_stake` e `notes`.

`--force` permite nova linha para item já presente. Isso não transforma a linha
mais recente em autoridade nem resolve divergências automaticamente.

Antes de retomar, o arquivo existente é lido integralmente e **cada linha** é
validada contra `tools/schemas/lpai-proxy-record.schema.json`. Linha fora do
schema, JSON inválido, UTF-8 inválido ou última linha sem newline encerram a
execução antes da criação do cliente e de qualquer download; o script nunca
concatena uma linha nova a JSONL truncado.

Os bytes atuais do schema são relidos no início de cada operação de validação e
novamente imediatamente antes do append. A construção do validator é reutilizada
somente quando esses bytes são idênticos; substituir ou remover o schema faz a
operação falhar, sem conservar resultado associado apenas ao caminho.

## Segurança de escrita

As barreiras são avaliadas antes de criar cliente ou realizar chamada de rede.
O destino:

1. deve terminar em `.jsonl`;
2. deve resolver fisicamente sob `data/staging/`;
3. não pode escapar com `..` ou por link simbólico;
4. não pode usar nomes de artefatos canônicos, como `records.jsonl`,
   `purification.jsonl` ou `corpus-data.json`;
5. não pode estar em `data/processed/`, `corpus/`, `examples/`, `schema/` ou
   `tools/schemas/`.

Na gravação, staging e cada ancestral são abertos por descritor com
`O_DIRECTORY`/`O_NOFOLLOW`; o arquivo final também usa `O_NOFOLLOW`, precisa ser
regular, precisa ter exatamente um link e não pode compartilhar dispositivo e
inode com nenhum artefato canônico conhecido. Isso bloqueia hardlinks e mantém
a barreira mesmo se um caminho for trocado depois da validação inicial.
Violação retorna código 3 e não cria nem trunca saída. Não há variável de
ambiente para mudar a raiz permitida de staging.

O cache de imagens segue a mesma política no-follow. Downloads entram em arquivo
temporário exclusivo e só são renomeados atomicamente após validação de tamanho,
MIME, assinatura, contagem de links e identidade do inode.

A decisão “item já gravado?” e o append ocorrem sob `flock` POSIX exclusivo no
descritor da saída. A linha inteira usa uma única chamada `os.write`; escrita
parcial é rejeitada e revertida ao tamanho anterior. Assim, duas execuções sem
`--force` não intercalam linhas nem gravam o mesmo `item_id` duas vezes. Com
`--force`, duplicidade é deliberadamente permitida.

Essas garantias dependem de `openat`/`dir_fd`, `O_NOFOLLOW` e `flock`; portanto,
o codificador operacional é suportado em sistemas POSIX. Não execute esta
versão em Windows nativo.

## Adjudicação humana

A saída não deve ser copiada ou mesclada automaticamente em:

- `data/processed/records.jsonl`;
- `data/processed/purification.jsonl`;
- `corpus/corpus-data.json`;
- qualquer export público.

Revise evidência, dúvidas, confiança, dados negativos e justificativa por item.
Registre a decisão humana em fluxo separado e mantenha a autoria do proxy apenas
como proveniência. Este script não implementa promoção.

## Códigos de saída

| Código | Significado |
| --- | --- |
| 0 | sucesso; sem baixa confiança detectada |
| 1 | erro de I/O, instrumento, schema, cliente ou API |
| 2 | execução concluída com baixa confiança/NC ou um ou mais itens pulados por falta de evidência |
| 3 | barreira de escrita rejeitou o destino antes da rede |

## Troubleshooting

### `codebook não encontrado`

Confirme:

```bash
test -f docs/methodology/codebooks/codebook-MASTER.md
```

### `master prompt (§16) não encontrado`

Não copie o prompt para o Python. Corrija a seção 16 na fonte editorial e
registre a mudança de `codebook_version` no próprio codebook.

### `saída deve ficar sob .../data/staging`

Remova `--output` ou use um caminho `.jsonl` dentro de `data/staging/`. Links
simbólicos para fora são recusados.

### `defina MOONSHOT_API_KEY no ambiente`

Exporte a chave somente para execução real. Para validar sem credencial, use
`--dry-run`.

### item sem imagem

Forneça `--images-dir` com arquivo nomeado pelo UUID, ou confirme que a URL do
registro aponta para uma imagem pública direta. A extensão da URL não é
suficiente: MIME e assinatura precisam corresponder. Sem `--allow-textual`, cada
item sem evidência é pulado e a execução retorna 2 — inclusive quando todos são
pulados. Não trate descrição textual como recepção histórica ou observação
visual sem declarar a limitação.

### `JSONL truncado`, `JSON inválido` ou `linha fora do schema`

Não edite por concatenação. Preserve o arquivo para auditoria, corrija-o
explicitamente ou escolha um novo nome `.jsonl` sob `data/staging/`. A falha
acontece antes de cliente e rede.

### argumento inválido

`--items` exige ao menos um ID; `--limit` deve ser maior que zero; `--retries`
aceita zero, mas não valor negativo. O `argparse` encerra com código 2 antes de
ler o corpus ou tocar a rede.

## Testes

```bash
python -m pytest tests/test_lpai_proxy_coder_k3.py -q --tb=short
```
