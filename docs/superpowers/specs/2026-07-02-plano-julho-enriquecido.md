# JULHO 2026 — O Grande Jogo das Alegorias 🃏 (Versão Enriquecida)

> Enriquecido por Safo (Hermes) a partir das sessões, estados reais de disco/repo/corpus, e pitfalls conhecidos.
> Spec original: `docs/superpowers/specs/2026-07-02-plano-julho-jogo-alegorias-design.md`

---

## ATO I — A FAXINA E A FUNDAÇÃO (Dias 01 a 05)

### ## PRÓLOGO — Carta 0: A Zeladora 🧹

**Objetivo:** Limpar o disco (2.1% livre) e reacender os 3 vigias adormecidos.
**Duração:** 1 dia. **Desbloqueia:** o mês inteiro.

#### Diagnóstico real (estado em 02/jul)

| O que | Estado atual |
|---|---|
| **Disco** | ~2.1% livre (crítico) |
| **Home permissions** | `~` estava 777 — precisa `chmod 700` |
| **Cron jobs** | 3 pausados: `claude-hermes-sync`, watchers de disco, watchers de corpus |
| **SSD externo** | `/Volumes/Sem Título/macOS_Expansion/` disponível, montado |
| **pip openai** | Quebrado (SSL/DNS em conda env) |
| **Vault path** | Real: `~/Obsidian/vida-os` (não o path antigo dos docs) |
| **Python** | conda env `iconocracy` em `/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/` |

#### Checklist executável

```bash
# 1. Corrigir permissões do home
chmod 700 ~

# 2. Offload para SSD — pastas pesadas
# Caches que podem ir pro SSD (já configurado no .zshrc com condicionais):
#   ~/.npm, ~/.cache, HF_HOME
# Conferir se o SSD está montado:
ls /Volumes/Sem\ Título/macOS_Expansion/

# Pastas candidatas a offload (verificar tamanho antes):
du -sh ~/Downloads ~/.cache ~/Library/Caches ~/.npm

# 3. Reacender cron jobs
# Listar jobs pausados via Hermes:
#   cronjob action='list'
# Para cada um pausado: cronjob action='resume', job_id='...'

# 4. Consertar pip openai
conda activate iconocracy
pip install openai --no-cache-dir

# 5. Verificar path do vault
ls -d ~/Obsidian/vida-os
# Se ok, atualizar referências nos docs que apontam pro path antigo
```

#### Pitfalls conhecidos

- **Disco cheio demais → offload falha.** Se `rsync` não tiver espaço pra metadata, usar `mv` (mesmo filesystem, instantâneo) ou offload em lotes pequenos (1 pasta por vez).
- **Cron jobs pausados há semanas** podem ter acumulado backlog. Verificar se não vão disparar tudo de uma vez ao resumir.
- **pip openai** pode falhar com SSL em ambiente conda no macOS 26. Desabilitar sandbox com `--no-sandbox` no pip se necessário, ou usar `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org openai`.
- **Home 777** é falha de segurança. Corrigir ANTES de qualquer outra operação.

#### Verificação de conclusão

- [ ] `df -h /` mostra >15% livre
- [ ] `ls -la ~ | head -3` mostra `drwx------` (700)
- [ ] `cronjob action='list'` mostra jobs ativos (não `paused`)
- [ ] `pip show openai` retorna versão instalada
- [ ] `ls -d ~/Obsidian/vida-os` existe

---

### ## Carta 1: A Restauradora 🎨

**Objetivo:** Curar os registros sem `purificacao` e exorcizar os duplicados reais (gêmeos falsos).
**Duração:** 2 dias. **Desbloqueia:** A Juíza.

#### Diagnóstico real (estado em 02/jul)

- **Registros sem purificação:** `code_purification.py --status` revelou que na verdade existem **92 itens sem purificação** (328 total - 236 codificados). A estimativa original de 41 registros estava desatualizada!
- **Gêmeos falsos (Colisões de hash):** Encontramos exatamente **4 colisões de hash** no corpus (`records.jsonl`). A análise detalhada revelou uma divisão crítica:

##### A) Duplicados Reais (Exorcismo imediato — remover um de cada par)
1. Poster **"Wake up America!"**
   - ID `39ebfe77-0d0b-5130-8cce-f6f48d85a081` vs ID `82c0efc9-1a2e-55a3-8eca-5de3e58a2fac`
   - URL idêntica, título igual (variação de maiúsculas).
2. Poster **"3e Emprunt de la Défense nationale"**
   - ID `2b7a1a18-1a29-5703-9264-6012425c65e8` vs ID `68a00893-7b89-5e58-8aef-79f89b547974`
   - URL idêntica, títulos ligeiramente diferentes (com/sem parênteses).

##### B) Falsos Duplicados (Colisões de hash de itens legítimos — corrigir hash generator)
1. **Revista Illustrada (16 nov. 1889)**
   - ID `e550331b-19c0-5ccb-b8ab-100a35c8a441` ("Alegoria da República") vs ID `8d89996e-c2aa-5a2e-a462-26b91f5308e4` ("A República nos braços de Floriano").
   - Compartilham a mesma URL porque a Hemeroteca Digital indexa o volume/edição sob um único link, mas as figuras são gravuras completamente distintas.
2. **Série Imperiale (Regno d'Italia)**
   - ID `09f8d8d5-4d94-5225-aa60-9827a8bf1c08` (Selo de 10 Lire) vs ID `bc06d4cc-455f-530e-b86b-e046378979a3` (Selo de 2 Lire).
   - Compartilham o mesmo URL de post de blog, mas representam selos de valores e feições iconográficas diferentes.

#### Checklist executável

```bash
# 1. Exorcizar os Duplicados Reais
# Remover uma das linhas de "Wake up America" (id 82c0efc9...) e "3e Emprunt" (id 68a00893...) de:
#   data/processed/records.jsonl
#   (Fazer backup antes de editar!)

# 2. Corrigir Colisão dos Falsos Duplicados
# Ajustar a função de geração de hash em:
#   tools/scripts/csv_to_records.py, ingest_fichas_lpai.py e vault_sync.py
# Modificação: se a URL for idêntica, concatenar um slug derivado do título ao input da hash sha256.

# 3. Rodar a validação do corpus
python tools/scripts/validate_schemas.py

# 4. Codificar os 92 itens restantes
# O ideal para não cansar é rodar em blocos por país:
python tools/scripts/code_purification.py --batch BR  # codifica o bloco do Brasil
python tools/scripts/code_purification.py --resume    # continua de onde parou interativamente
```

#### Pitfalls conhecidos

- **Interface Interativa:** `code_purification.py` requer input humano linha a linha. Certifique-se de rodar no terminal com suporte a PTY (ou no terminal integrado do app) e nunca em tarefas de cron não-interativas.
- **Drift de IDs:** Se deletar itens do corpus, certifique-se de que os arquivos correspondentes em `vault/candidatos/` também sejam atualizados/removidos para evitar órfãos.

#### Verificação de conclusão

- [ ] `records.jsonl` validado sem erros via `validate_schemas.py`
- [ ] 0 duplicados reais remanescentes nos hashes do corpus
- [ ] `code_purification.py --status` mostra 0 itens restantes (ou em progresso controlado)

---

### ## Carta 2: A Agrimensora 📐

**Objetivo:** Re-rodar as análises estatísticas dos notebooks (05 a 08) usando a totalidade do corpus N=328 (anteriormente N=165).
**Duração:** 2 dias. **Desbloqueia:** A Escrivã.

#### Diagnóstico real (estado em 02/jul)

Os seguintes notebooks residem em `notebooks/`:
- `05_temporal.ipynb` (análise de evolução histórica)
- `06_clustering.ipynb` (agrupamento dos regimes iconocráticos)
- `07_dimensionality.ipynb` (redução de dimensionalidade, PCA)
- `08_multidimensional_scoring.ipynb` (cálculo de scores compostos de endurecimento)

Eles estavam travados usando um subset antigo de N=165. Com o corpus canônico completo e purificado de N=328, os agrupamentos e trajetórias históricas podem mudar de forma dramática!

#### Checklist executável

```bash
# 1. Entrar no conda env
conda activate iconocracy

# 2. Re-gerar o CSV canônico consolidado (dataset base das análises)
python tools/scripts/code_purification.py --export-csv

# 3. Abrir e executar os notebooks sequencialmente
# Você pode rodá-los via CLI se preferir para uma execução rápida:
jupyter nbconvert --to notebook --execute --inplace notebooks/05_temporal.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/06_clustering.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/07_dimensionality.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/08_multidimensional_scoring.ipynb

# 4. Verificar se os plots foram gerados em notebooks/output/ ou notebooks/plots/
```

#### Pitfalls conhecidos

- **Dependências de visualização:** Alguns notebooks usam `matplotlib`, `seaborn` ou `scikit-learn` que podem ter tido quebras de API no Python 3.12. Rodar um primeiro teste antes de executar todos de uma vez.
- **Drift de resultados:** Se o PCA/Clustering alterar a distribuição dos três regimes principais (Fundacional, Modernista, Contemporâneo), o argumento do Capítulo 6 terá que ser ligeiramente modulado para refletir a nova realidade empírica. Isso é ciência de verdade!

#### Verificação de conclusão

- [ ] `data/processed/corpus_dataset.csv` gerado com N=328 registros
- [ ] Notebooks 05, 06, 07 e 08 executados de ponta a ponta sem erros
- [ ] Novos gráficos salvos e prontos para inspeção visual
