---
title: "Plano de Estudos — Book of Secret Knowledge"
aliases:
  - plano-sysadmin
  - estudos-devops
  - roadmap-security
tags:
  - estudos/sysadmin
  - estudos/devops
  - estudos/security
  - projeto/autodesenvolvimento
status: ativo
created: "2026-04-15"
updated: "2026-04-15"
---

# Plano de Estudos — Book of Secret Knowledge

> [!info] Sobre este plano
> Roteiro de **4 semanas** baseado no repositório [The Book of Secret Knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) — uma coleção curada de recursos para SysAdmins, DevOps Engineers, Pentesters e Security Researchers. Cada semana foca em uma área temática com progressão lógica.

---

## Semana 1: CLI Fundamentals

> [!goal] Objetivo
> Dominar ferramentas de linha de comando essenciais, configurar ambiente de trabalho eficiente e internalizar fluxos de produtividade no terminal.

### Tópicos

#### Shells & Configuração
- [ ] [GNU Bash](https://www.gnu.org/software/bash/) — shell padrão, estudar expansões e scripting básico
- [ ] [Zsh](https://www.zsh.org/) + [Oh My ZSH](https://ohmyz.sh/) — shell moderno com plugins
- [ ] [fish](https://fishshell.com/) — alternativa user-friendly com autosuggestions
- [ ] [starship](https://starship.rs/) — prompt minimalista e rápido

#### Text Editors (terminal)
- [ ] [Vim](https://www.vim.org/) — editor modal, aprender movimentação e modos básicos
- [ ] [micro](https://micro-editor.github.io/) — alternativa moderna com keybindings intuitivos
- [ ] [bat](https://github.com/sharkdp/bat) — `cat` com syntax highlighting

#### File Management & Navigation
- [ ] [ranger](https://github.com/ranger/ranger) — file manager com preview
- [ ] [nnn](https://github.com/jarun/nnn) — file manager minimalista e rápido
- [ ] [fzf](https://github.com/junegunn/fzf) — fuzzy finder (==essencial==)
- [ ] [fd](https://github.com/sharkdp/fd) — alternativa moderna ao `find`
- [ ] [ripgrep (rg)](https://github.com/BurntSushi/ripgrep) — grep ultrarrápido

#### Produtividade
- [ ] [tmux](https://github.com/tmux/tmux/wiki) — multiplexador de terminal
- [ ] [screen](https://www.gnu.org/software/screen/) — alternativa clássica ao tmux
- [ ] [z](https://github.com/rupa/z) — jump rápido entre diretórios frequentes

### Guias de Estudo
- [ ] [Bash Guide](https://mywiki.wooledge.org/BashGuide) — guia completo de Bash
- [ ] [The Art of Command Line](https://github.com/jlevy/the-art-of-command-line) — fundamentos essenciais
- [ ] [Bash Hackers Wiki](https://wiki.bash-hackers.org/start) — referência avançada

### Exercícios Práticos
1. Configurar Zsh + Oh My ZSH + starship no ambiente local
2. Aprender 20 comandos Vim essenciais (movimento, edição, busca)
3. Criar aliases úteis no `.zshrc` / `.bashrc`
4. Usar `fzf` integrado com histórico de comandos (`Ctrl+R`)
5. Navegar projeto complexo usando apenas `ranger` ou `nnn`

---

## Semana 2: Networking & Systems

> [!goal] Objetivo
> Compreender protocolos de rede, ferramentas de diagnóstico e administração de sistemas Linux. Foco em one-liners práticos.

### Tópicos

#### Network Diagnostics
- [ ] [tcpdump](https://www.tcpdump.org/) — captura de pacotes (==fundamental==)
- [ ] [Wireshark](https://www.wireshark.org/) — análise gráfica de tráfego
- [ ] [nmap](https://nmap.org/) — scanner de rede e portas
- [ ] [netcat (nc)](http://netcat.sourceforge.net/) — "canivete suíço" de rede
- [ ] [mtr](https://github.com/traviscross/mtr) — traceroute + ping combinados
- [ ] [iftop](http://www.interhack.net/projects/iftop/) — monitor de bandwidth em tempo real

#### DNS Tools
- [ ] [dig](https://linux.die.net/man/1/dig) — queries DNS detalhadas
- [ ] [dog](https://github.com/ogham/dog) — alternativa moderna ao dig
- [ ] [dnstracer](http://www.mavetju.org/unix/dnstracer.php) — trace de resolução DNS

#### SSH Mastery
- [ ] SSH tunneling (local/remote port forwarding)
- [ ] SSH jump hosts (`ProxyJump`)
- [ ] `ssh-agent` e keychain management
- [ ] Configuração avançada em `~/.ssh/config`

#### System Administration
- [ ] `ps`, `top`, `htop` — monitoramento de processos
- [ ] `lsof` — arquivos abertos e conexões
- [ ] `strace` / `ltrace` — tracing de syscalls
- [ ] `vmstat`, `iostat`, `sar` — métricas de sistema
- [ ] `journalctl` — logs do systemd

### One-liners Essenciais (do repositório)

```bash
# Listar conexões estabelecidas
netstat -tunap | grep ESTABLISHED

# Capturar tráfego HTTP
tcpdump -i any -A -s 0 'tcp port 80'

# Scan rápido de rede local
nmap -sn 192.168.1.0/24

# SSH tunnel (local port forward)
ssh -L 8080:localhost:80 user@remote

# Encontrar processo usando porta
lsof -i :8080
```

### Guias de Estudo
- [ ] [Linux Performance](http://www.brendangregg.com/linuxperf.html) — Brendan Gregg
- [ ] [SSH Mastery](https://www.tiltedwindmillpress.com/product/ssh-mastery-2nd-edition/) — referência completa
- [ ] [Nmap Network Scanning](https://nmap.org/book/) — guia oficial

### Exercícios Práticos
1. Capturar e analisar handshake TCP com `tcpdump`
2. Configurar SSH config com múltiplos hosts e jump server
3. Criar tunnel SSH para acessar serviço remoto
4. Escanear rede local e identificar serviços com `nmap`
5. Monitorar performance de sistema sob carga com `htop` + `iostat`

---

## Semana 3: Security & endurecimento

> [!goal] Objetivo
> Fundamentos de segurança, criptografia prática, e introdução a pentesting. Foco em ferramentas defensivas e ofensivas básicas.

### Tópicos

#### Criptografia Prática
- [ ] [OpenSSL](https://www.openssl.org/) — operações SSL/TLS, certificados, hashing
- [ ] [GPG](https://gnupg.org/) — criptografia e assinaturas
- [ ] [age](https://github.com/FiloSottile/age) — alternativa moderna ao GPG

#### SSL/TLS Tools
- [ ] [testssl.sh](https://github.com/drwetter/testssl.sh) — teste de configuração TLS
- [ ] [sslscan](https://github.com/rbsec/sslscan) — scanner de SSL
- [ ] [SSL Labs](https://www.ssllabs.com/ssltest/) — análise online

#### Network Security
- [ ] [hping3](http://www.hping.org/) — packet crafter (==poderoso==)
- [ ] [socat](http://www.dest-unreach.org/socat/) — relay multipropósito
- [ ] [p0f](https://lcamtuf.coredump.cx/p0f3/) — fingerprinting passivo

#### Security Analysis
- [ ] [Lynis](https://cisofy.com/lynis/) — auditoria de sistema
- [ ] [OSSEC](https://www.ossec.net/) — HIDS
- [ ] [ClamAV](https://www.clamav.net/) — antivírus open source

#### Web Security Basics
- [ ] [OWASP Top 10](https://owasp.org/www-project-top-ten/) — vulnerabilidades mais comuns
- [ ] [Burp Suite Community](https://portswigger.net/burp/communitydownload) — proxy de interceptação
- [ ] [OWASP ZAP](https://www.zaproxy.org/) — alternativa open source

### One-liners de Segurança (do repositório)

```bash
# Gerar senha aleatória
openssl rand -base64 32

# Verificar certificado de site
openssl s_client -connect example.com:443 -servername example.com

# Hash de arquivo (verificação de integridade)
sha256sum arquivo.txt

# Criptografar arquivo com GPG
gpg -c --cipher-algo AES256 arquivo.txt

# Secure delete
shred -vfz -n 5 arquivo.txt

# Testar cipher suites de servidor
nmap --script ssl-enum-ciphers -p 443 example.com
```

### Guias de Estudo
- [ ] [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) — metodologia de testes
- [ ] [Hacking: The Art of Exploitation](https://nostarch.com/hacking2.htm) — fundamentos
- [ ] [Linux endurecimento Guide](https://madaidans-insecurities.github.io/guides/linux-hardening.html) — hardening completo

### Exercícios Práticos
1. Gerar certificado autoassinado com OpenSSL
2. Configurar GPG keypair e assinar/criptografar arquivo
3. Auditar sistema local com Lynis e corrigir findings críticos
4. Usar Burp Suite para interceptar tráfego HTTP de aplicação
5. Testar configuração TLS de servidor com `testssl.sh`

---

## Semana 4: DevOps & Labs Práticos

> [!goal] Objetivo
> Containerização, orquestração e prática hands-on em ambientes de CTF e labs de segurança.

### Tópicos

#### Docker
- [ ] [Docker](https://www.docker.com/) — fundamentos de containers
- [ ] [dive](https://github.com/wagoodman/dive) — explorar layers de imagens
- [ ] [lazydocker](https://github.com/jesseduffield/lazydocker) — TUI para Docker
- [ ] [hadolint](https://github.com/hadolint/hadolint) — linter de Dockerfiles
- [ ] [Trivy](https://github.com/aquasecurity/trivy) — scanner de vulnerabilidades

#### Kubernetes
- [ ] [kubectl](https://kubernetes.io/docs/reference/kubectl/) — CLI oficial
- [ ] [k9s](https://k9scli.io/) — TUI para Kubernetes (==excelente==)
- [ ] [kubectx/kubens](https://github.com/ahmetb/kubectx) — troca rápida de contexto
- [ ] [stern](https://github.com/stern/stern) — tail de logs multi-pod

#### Infrastructure as Code
- [ ] [Terraform](https://www.terraform.io/) — IaC declarativo
- [ ] [Ansible](https://www.ansible.com/) — automação e configuração

### Plataformas de Prática (CTF & Labs)

> [!tip] Prioridade
> Começar pelo **OverTheWire Bandit** (gratuito, fundamentos Linux) e depois avançar para plataformas mais complexas.

- [ ] [OverTheWire](https://overthewire.org/wargames/) — wargames gratuitos
  - **Bandit** — fundamentos Linux (==começar aqui==)
  - **Natas** — web security basics
  - **Leviathan** — privilege escalation
- [ ] [Hack The Box](https://www.hackthebox.com/) — máquinas vulneráveis
- [ ] [TryHackMe](https://tryhackme.com/) — learning paths guiados
- [ ] [PentesterLab](https://pentesterlab.com/) — exercícios web security
- [ ] [VulnHub](https://www.vulnhub.com/) — VMs vulneráveis para download

### Cheat Sheets Úteis
- [ ] [Docker Cheat Sheet](https://github.com/wsargent/docker-cheat-sheet)
- [ ] [Kubernetes Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [ ] [Reverse Shell Cheat Sheet](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)

### Exercícios Práticos
1. Criar Dockerfile otimizado para aplicação Python/Node
2. Escanear imagem Docker com Trivy e corrigir vulnerabilidades
3. Completar **Bandit** níveis 0-15 no OverTheWire
4. Resolver uma máquina "Easy" no Hack The Box ou TryHackMe
5. Subir cluster local com `kind` ou `minikube` e explorar com `k9s`

---

## Recursos Complementares

### Blogs & Sites de Referência
- [Brendan Gregg's Blog](http://www.brendangregg.com/) — performance Linux
- [Julia Evans (b0rk)](https://jvns.ca/) — zines e explicações visuais
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials) — guias práticos
- [Ars Technica](https://arstechnica.com/) — notícias tech

### Newsletters
- [DevOps Weekly](https://www.devopsweekly.com/)
- [SRE Weekly](https://sreweekly.com/)
- [tl;dr sec](https://tldrsec.com/) — security newsletter

### Podcasts
- [Darknet Diaries](https://darknetdiaries.com/) — histórias de hacking
- [Command Line Heroes](https://www.redhat.com/en/command-line-heroes) — história de tech

---

## Cronograma Sugerido

| Semana | Foco | Horas/dia | Entregável |
|--------|------|-----------|------------|
| 1 | CLI Fundamentals | 1-2h | Ambiente configurado + aliases úteis |
| 2 | Networking & Systems | 1-2h | SSH config avançado + one-liners documentados |
| 3 | Security & endurecimento | 1-2h | Sistema auditado + GPG configurado |
| 4 | DevOps & Labs | 2-3h | Bandit 0-15 completo + 1 máquina HTB/THM |

---

## Conexões

- [[Estudos de Programação]] %% se existir %%
- [[Projetos de Infraestrutura]] %% se existir %%

---

## Próximos passos

- [ ] Iniciar Semana 1 — configurar ambiente de terminal
- [ ] Criar notas individuais para ferramentas mais complexas (Vim, tmux, nmap)
- [ ] Documentar one-liners úteis em nota separada
- [ ] Agendar sessões de estudo no calendário

---

%% Plano criado a partir do repositório The Book of Secret Knowledge (https://github.com/trimstray/the-book-of-secret-knowledge). Recursos selecionados para progressão lógica de CLI → Networking → Security → DevOps. %%
