# Obsidian Git — Setup Guide

> Configura auto-commit do vault Obsidian para o repositório `anavvanzin/iconocracy-corpus`.
> Como o vault vive **dentro** do repo (`vault/`), o Obsidian Git faz commit de tudo — notas, templates, e dados.

---

## Pré-requisitos

1. **Git** instalado no Mac (`git --version` no Terminal)
2. **GitHub SSH key** configurada (`ssh -T git@github.com` deve funcionar)
3. O repo `iconocracy-corpus` já clonado localmente
4. **Obsidian** instalado com o vault aberto em `vault/`

---

## Passo 1: Instalar o plugin

1. Obsidian → Settings (⌘ ,) → Community plugins → Browse
2. Buscar **"Obsidian Git"** (autor: Vinzent03)
3. Install → Enable

---

## Passo 2: Configurar o plugin

Settings → Community plugins → Obsidian Git → ⚙️

### Configurações recomendadas

| Configuração | Valor | Por quê |
|---|---|---|
| **Vault backup interval (minutes)** | `30` | Auto-commit a cada 30 min enquanto Obsidian está aberto |
| **Auto pull interval (minutes)** | `0` | Desligar — você é a única autora. Evita conflitos |
| **Commit message** | `vault: {{date}}` | Mensagem limpa com timestamp |
| **Date format** | `YYYY-MM-DD HH:mm` | ISO-like |
| **Push on backup** | `✓ ON` | Envia para GitHub automaticamente após cada commit |
| **Pull changes before push** | `✓ ON` | Segurança: pull antes de push |
| **Disable on this device** | `OFF` | Manter ligado |
| **Auto backup after file change** | `OFF` | O intervalo de 30 min é suficiente |
| **Show status bar** | `✓ ON` | Mostra último sync no rodapé |

### Avançado

| Configuração | Valor |
|---|---|
| **Custom base path (relative to vault)** | `..` |

> **IMPORTANTE:** Como o vault está em `repo/vault/` mas o `.git/` está em `repo/`,
> o plugin precisa saber que o repositório Git está **um nível acima** do vault.
> Defina **Custom base path** como `..` para que o Obsidian Git encontre o `.git/`.

---

## Passo 3: Testar

1. Crie uma nota de teste no vault (ex: `00-inbox/teste-git.md`)
2. No Obsidian, abra o command palette (⌘ P)
3. Digite **"Obsidian Git: Commit all changes"**
4. Verifique no Terminal: `cd /caminho/do/repo && git log -1`
5. Verifique no GitHub: a nota deve aparecer em `vault/00-inbox/`
6. Delete a nota de teste

---

## Passo 4: .gitignore

Garanta que o `.gitignore` do repo inclua:

```gitignore
# Obsidian workspace (pessoal, não versionar)
vault/.obsidian/workspace.json
vault/.obsidian/workspace-mobile.json

# Obsidian cache
vault/.obsidian/cache

# Thumbnails gerados
vault/.obsidian/plugins/*/data.json

# macOS
.DS_Store

# SSD symlink targets (binários ficam no SSD, não no Git)
data/raw/BR/
data/raw/FR/
data/raw/UK/
data/raw/DE/
data/raw/US/
data/raw/BE/
```

> Não ignore `vault/.obsidian/` inteiro — as configs de plugins (Dataview, Templater, etc.) devem ser versionadas para reprodutibilidade.

---

## Passo 5: Hotkeys úteis

Configurar em Settings → Hotkeys:

| Ação | Sugestão de tecla |
|---|---|
| Obsidian Git: Commit all changes | `⌘ ⇧ G` |
| Obsidian Git: Push | `⌘ ⇧ P` |
| Obsidian Git: Open source control view | `⌘ ⇧ S` |

---

## Fluxo no dia a dia

O plugin cuida de tudo automaticamente:

1. Você trabalha normalmente no Obsidian
2. A cada 30 min, o plugin faz commit + push silencioso
3. O status bar mostra "Last backup: HH:MM"
4. Se quiser forçar um sync (ex: antes de fechar o laptop), use ⌘⇧G

Para commits mais significativos (ex: após uma sessão Scout completa), use o Terminal:

```bash
cd /caminho/do/repo
git add -A
git commit -m "corpus: +5 candidatos FR após campanha 3"
git push
```

---

## Troubleshooting

### "Cannot find .git directory"
→ Verificar que **Custom base path** está definido como `..`

### "Permission denied (publickey)"
→ SSH key não está configurada. No Terminal:
```bash
ssh-keygen -t ed25519 -C "ana.vanzin@posgrad.ufsc.br"
cat ~/.ssh/id_ed25519.pub
# Copiar e colar em GitHub → Settings → SSH keys
```

### "Merge conflict"
→ Raro (você é a única autora), mas se acontecer:
```bash
cd /caminho/do/repo
git status       # ver arquivos em conflito
git checkout --theirs vault/arquivo.md  # manter versão remota
# OU
git checkout --ours vault/arquivo.md    # manter versão local
git add . && git commit -m "resolve conflict"
```

### Plugin não aparece
→ Verificar: Settings → Community plugins → "Restricted mode" deve estar **OFF**

---

## Integração com vault-to-jsonl.py

Após sessões de catalogação, o fluxo completo é:

```bash
cd /caminho/do/repo

# 1. Sync vault → records.jsonl
python3 tools/scripts/vault-to-jsonl.py --diff

# 2. Commit tudo (notas + jsonl atualizado)
git add vault/ data/processed/records.jsonl
git commit -m "corpus: sync vault → records.jsonl"
git push
```

Ou deixar o Obsidian Git cuidar das notas e só rodar o sync script manualmente quando precisar atualizar o records.jsonl.

---

*Guia criado em abril de 2026 · Projeto ICONOCRACY · Ana Vanzin · PPGD/UFSC*
