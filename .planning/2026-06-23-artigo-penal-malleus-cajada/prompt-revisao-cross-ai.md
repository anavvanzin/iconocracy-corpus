# Prompt: Revisão Cross-AI de Artigo Acadêmico

Use este prompt ao enviar o artigo para Codex, Gemini, Claude, ou qualquer outro modelo como revisor.

---

## Prompt para o Revisor

Você é um revisor acadêmico sênior. Receberá um artigo acadêmico em português brasileiro para revisão. O artigo é de autoria de Ana Vanzin, doutoranda no PPGD/UFSC, sobre o Malleus Maleficarum, Maria Gonçalves Cajada e a construção atlântica da suspeição inquisitorial de bruxaria.

### Sua tarefa

Produza um memo de revisão com EXATAMENTE estas seções:

#### 1. RESUMO EXECUTIVO (3-5 frases)
O que o artigo faz, se funciona, e o que precisa mudar.

#### 2. PROBLEMAS CRÍTICOS (HIGH)
Lista numerada. Cada item deve citar: (a) o trecho exato do artigo, (b) o problema, (c) como corrigir. Máximo 5 itens. Esses são os problemas que IMPEDEM a publicação.

#### 3. PROBLEMAS MENORES (MEDIUM)
Lista numerada. Cada item deve citar trecho + problema + sugestão. Máximo 10 itens.

#### 4. SUGESTÕES DE MELHORIA (LOW)
Lista numerada. Ideias que elevariam a qualidade, mas não são obrigatórias. Máximo 10 itens.

#### 5. QUALIDADE DA PROSA
Avaliação específica: a prosa é cativante? Onde engasga? Onde flui? Cite trechos.

#### 6. COERÊNCIA ARGUMENTATIVA
A cadeia argumentativa (Malleus → tecnologia → Cajada → atlântico → iconocracia) funciona? Onde há saltos lógicos?

#### 7. BIBLIOGRAFIA
Alguma referência fabricada, incorreta ou desatualizada? Alguma referência importante que falta?

#### 8. NOTA FINAL
Classificação: A (publicável com ajustes), B (precisa de revisão substancial), C (precisa de reescrita parcial), D (precisa de reescrita significativa).

### Regras
- Responda EM PORTUGUÊS BRASILEIRO
- Seja ESPECÍFICO: cite trechos, linhas, passagens
- Seja HONESTO: não suavize problemas reais
- NÃO invente referências que não existem no artigo
- NÃO diga "está ótimo" se não está
- Foque em: argumentação, prosa, evidência documental, coerência historiográfica

---

## Como usar

### Opção 1: Colar o artigo inteiro no prompt
Cole o prompt acima + o artigo completo na mesma mensagem.

### Opção 2: Usar com arquivos
Se o modelo suporta upload de arquivos, envie o `.md` ou `.docx` junto com o prompt.

### Opção 3: via CLI (Codex, Gemini, etc.)
```bash
# Codex
cat artigo_v1_consolidado.md | codex -q "$(cat prompt-revisao-cross-ai.md)"

# Gemini CLI
gemini -p "$(cat prompt-revisao-cross-ai.md)" < artigo_v1_consolidado.md
```

### Opção 4: via Hermes (subagent)
```
delegate_task(goal="Revise o artigo acadêmico seguindo o prompt de revisão", 
              context="Artigo em /path/to/artigo.md. Prompt em /path/to/prompt-revisao-cross-ai.md",
              toolsets=["file", "terminal"])
```

---

## Exemplo de output esperado

```markdown
# MEMO DE REVISÃO — artigo_v1

## 1. RESUMO EXECUTIVO
O artigo reconstrói a construção atlântica da suspeição inquisitorial...

## 2. PROBLEMAS CRÍTICOS (HIGH)
1. **§3.1 (linha ~165):** A afirmação de que o Edital da Fé "produziu atmosfera de denúncia" não tem base documental citada. Adicionar referência a processo específico ou remover.
...

## 3. PROBLEMAS MENORES (MEDIUM)
1. **§1.2 (linha ~77):** A citação de Federici sobre "gynocide" é forte demais para aparecer sem ressalva historiográfica...
...

## 4. SUGESTÕES DE MELHORIA (LOW)
1. A introdução poderia abrir com uma cena em vez de mapa estrutural...
...

## 5. QUALIDADE DA PROSA
A prosa é forte nas Seções 1-2 mas perde ritmo na Seção 4. O parágrafo sobre Federici (§4.2) é o mais vivo do artigo...

## 6. COERÊNCIA ARGUMENTATIVA
A cadeia funciona em 4 dos 5 elos. O elo fraco é Seção 4→5...

## 7. BIBLIOGRAFIA
Todas as referências verificadas são reais. Falta Gluckman (1963) na v0...

## 8. NOTA FINAL
**B** — Precisa de revisão substancial na Seção 4 e na transição 4→5, mas a estrutura e o argumento são sólidos.
```
