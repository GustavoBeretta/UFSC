# Mini-Blockchain Simétrica com Autenticação de Usuário

**INE 5680 / INE410148 — Segurança da Informação e de Redes**  
UFSC — Departamento de Informática e Estatística

---

## O que é este projeto

Uma mini-blockchain multiusuário onde cada usuário pode registrar transações de forma segura. O sistema garante:

- **Confidencialidade** — dados de cada usuário são criptografados individualmente com AES-GCM
- **Autenticação forte** — cada usuário precisa de senha + TOTP (autenticação de dois fatores) para operar
- **Integridade da blockchain** — cada bloco depende do hash do bloco anterior, formando uma cadeia imutável
- **Multiusuário** — vários usuários podem adicionar blocos, mas cada um só decifra os seus próprios dados

---

## Requisitos

- Python 3.10 ou superior
- Biblioteca `cryptography`

---

## Instalação

**1. Verifique a versão do Python:**
```bash
python --version
```

**2. Instale a dependência:**
```bash
pip install cryptography
```

**3. Execute o programa:**
```bash
python3 mini_blockchain_pt.py
```

---

## Arquivos gerados automaticamente

| Arquivo | Conteúdo |
|---|---|
| `usuarios.json` | Dados de cadastro (sal em claro, TOTP e verificação de senha cifrados) |
| `blockchain.json` | Cadeia de blocos pública (dados dos blocos cifrados com AES-GCM) |

Esses arquivos são criados na mesma pasta do programa na primeira execução.

---

## Como usar

### Menu principal

Ao executar o programa você verá:

```
╔══════════════════════════════════════════════════════╗
║   Mini-Blockchain com Autenticação de Usuário        ║
║   INE 5680 – UFSC  |  PBKDF2 + AES-GCM + TOTP      ║
╚══════════════════════════════════════════════════════╝

=== MENU PRINCIPAL ===
  1. Cadastrar usuário
  2. Login
  3. Validar integridade da blockchain (sem login)
  4. Sair
```

---

### 1. Cadastrar usuário

Escolha a opção `1` e preencha:

```
Nome de usuário: alice
Senha: ********
Confirme a senha: ********
```

Requisitos da senha: mínimo 8 caracteres.

Ao finalizar o cadastro, o sistema exibe a **chave secreta TOTP**:

```
[TOTP] Configure seu autenticador (Google Authenticator, Authy, etc.)
       Chave secreta TOTP (Base32): JBSWY3DPEHPK3PXP
       Código atual para teste:     482931

[ATENÇÃO] Guarde a chave TOTP – ela não será exibida novamente.
```

> **Importante:** guarde essa chave Base32. Ela é necessária para configurar o autenticador e não será exibida novamente.

---

### Configurar o autenticador TOTP

Baixe o  **Authy** (Android / iOS) no celular

**Passos no Google Authenticator:**

1. Abra o app e toque em **+**
2. Escolha **Inserir uma chave de configuração**
3. Preencha:
   - Nome da conta: qualquer nome (ex: `Mini-Blockchain alice`)
   - Sua chave: cole a chave Base32 exibida no cadastro
   - Tipo: **Baseado em tempo**
4. Toque em **Adicionar**

O app vai gerar um código de 6 dígitos novo a cada 30 segundos.

> **Para testes rápidos:** o código atual é exibido no momento do cadastro. Se você digitá-lo imediatamente no login (dentro dos 30 segundos) funciona sem precisar do app.

---

### 2. Fazer login

Escolha a opção `2`:

```
=== LOGIN ===
Nome de usuário: alice
Senha: ********
Código TOTP (6 dígitos): 482931
```

Se a senha e o código estiverem corretos:

```
[OK] Login bem-sucedido. Bem-vindo, alice!
```

**Possíveis erros:**

| Mensagem | Causa |
|---|---|
| `[ERRO] Usuário não encontrado.` | Nome de usuário digitado errado |
| `[ERRO] Senha incorreta.` | Senha errada |
| `[ERRO] Código TOTP inválido ou expirado.` | Código expirou (aguarde o próximo) ou chave TOTP configurada errada |

---

### Menu do usuário autenticado

Após o login bem-sucedido:

```
=== MENU [alice] ===
  1. Adicionar bloco
  2. Listar blockchain (com decifragem dos meus blocos)
  3. Validar integridade da cadeia
  4. Logout
```

---

### Adicionar bloco

Escolha a opção `1`:

```
=== ADICIONAR BLOCO ===
Dados do bloco (transação/mensagem): Transferencia de 100 reais para João
```

Resultado:

```
[OK] Bloco #0 adicionado à blockchain.
     Hash: a3f9c2d1e8b74f2c9d3e1a5b7c8d9e0f...
```

Os dados são cifrados com **AES-256-GCM** antes de serem salvos. Ninguém consegue ler o conteúdo sem a senha do usuário.

---

### Listar blockchain

Escolha a opção `2`. O sistema mostra todos os blocos da cadeia, mas **só decifra os seus**:

```
=== BLOCKCHAIN (2 blocos) ===

Bloco #0
  Proprietário : alice
  Timestamp    : 2026-05-09T12:20:29.417440Z
  Hash         : c26f660e27bc0061d4b73bbdea28f37c...
  Hash Anterior: 0000000000000000000000000000000000...
  Integridade  : ✓ OK
  Dados        : Transferencia de 100 reais para João

Bloco #1
  Proprietário : bob
  Timestamp    : 2026-05-09T12:24:10.849845Z
  Hash         : b8c171f11b31ae0108ae656b6f0e6e1b...
  Hash Anterior: c26f660e27bc0061d4b73bbdea28f37c...
  Integridade  : ✓ OK
  Dados        : [cifrado – acesso negado]

[OK] Cadeia íntegra – todos os hashes válidos.
```

- Blocos seus aparecem com o conteúdo decifrado
- Blocos de outros usuários aparecem como `[cifrado – acesso negado]`

---

### Validar integridade da cadeia

Escolha a opção `3`. Não decifra nada, apenas verifica os hashes:

```
=== VALIDAÇÃO DA CADEIA (2 blocos) ===

  Bloco #0 [alice] ✓
  Bloco #1 [bob] ✓

[OK] Blockchain íntegra.
```

O `✓` em cada bloco confirma que:
- O `hash_anterior` bate com o hash real do bloco anterior
- O hash do próprio bloco não foi alterado

Essa opção está disponível também no **menu principal (opção 3)**, sem precisar de login.

---

## Testes de segurança

### Teste 1 — Senha incorreta no login

Digite uma senha errada ao fazer login:

```
[ERRO] Senha incorreta.
```

### Teste 2 — TOTP inválido no login

Digite um código TOTP errado ou expirado:

```
[ERRO] Código TOTP inválido ou expirado.
```

### Teste 3 — Acesso negado a blocos de outro usuário

Faça login com `alice`, adicione um bloco. Faça logout, faça login com `bob`, adicione um bloco. Faça logout e logue novamente com `alice`. Ao listar a blockchain, o bloco de `bob` aparece como:

```
Dados        : [cifrado – acesso negado]
```

### Teste 4 — Modificar ciphertext → falha de integridade AES-GCM

1. Abra o arquivo `blockchain.json` em qualquer editor de texto
2. Localize o campo `"dados"` de qualquer bloco e altere um caractere:
   ```json
   "dados": "xGkqHcABCD..."
   ```
3. Salve o arquivo
4. Faça login e escolha a opção `2 (Listar blockchain)`

Resultado esperado:

```
Bloco #0
  Integridade  : ✓ OK
  Dados        : [ERRO de decifragem – dados adulterados ou chave diferente]
```

O AES-GCM detecta que o ciphertext foi adulterado e recusa decifrar, mesmo que o hash do bloco ainda esteja OK.

### Teste 5 — Alterar hash_anterior → erro de validação da cadeia

1. Abra o `blockchain.json`
2. Localize o campo `"hash_anterior"` do bloco #1 e altere um caractere:
   ```json
   "hash_anterior": "0000000000000000000000000000000000000000000000000000000000000001"
   ```
3. Salve o arquivo
4. Execute o programa e escolha a opção `3 (Validar integridade)` no menu principal

Resultado esperado:

```
Bloco #0 [alice] ✓
Bloco #1 [bob] ❌
  → hash_anterior não bate com hash do bloco anterior!
  → hash do próprio bloco foi alterado!

[ERRO] Blockchain COMPROMETIDA – adulteração detectada!
```

O bloco #1 falha em dois pontos: o `hash_anterior` não bate com o hash real do bloco #0, e o `hash_bloco` do próprio bloco #1 também não bate mais, pois o campo `hash_anterior` faz parte do cálculo do hash.

---

## Conceitos criptográficos utilizados

### PBKDF2 (Password-Based Key Derivation Function 2)

Transforma a senha do usuário em uma chave criptográfica de 256 bits usando:
- **sal aleatório** de 32 bytes (armazenado em claro no `usuarios.json`)
- **600.000 iterações** de HMAC-SHA256 (recomendação NIST 2023)

A mesma senha + mesmo sal sempre produz a mesma chave — por isso blocos criados em sessões anteriores podem ser decifrados ao fazer login novamente.

### AES-256-GCM

Algoritmo de cifragem autenticada usado para proteger os dados de cada bloco:
- **Confidencialidade** — ninguém lê o conteúdo sem a chave
- **Integridade** — qualquer alteração no ciphertext é detectada pela tag GCM
- **IV único por bloco** — 96 bits gerados aleatoriamente, nunca reutilizados

### TOTP (Time-Based One-Time Password — RFC 6238)

Autenticação de dois fatores baseada em tempo:
- Código de 6 dígitos válido por 30 segundos
- Calculado como `HMAC-SHA1(chave_secreta, época_atual)`
- A chave secreta TOTP é armazenada **cifrada** com AES-GCM no `usuarios.json`
- Tolerância de ±1 época (90 segundos) para dessincronização de relógio

### Encadeamento por hash SHA-256

Cada bloco contém o hash SHA-256 do bloco anterior:
- Qualquer alteração em um bloco muda seu hash
- Isso invalida o `hash_anterior` de todos os blocos seguintes
- Adulterações são detectadas ao validar a cadeia

---

## Estrutura do blockchain.json

```json
[
  {
    "indice": 0,
    "proprietario": "alice",
    "timestamp": "2026-05-09T12:20:29.417440Z",
    "hash_anterior": "0000...0000",
    "sal_bloco": "<Salt em Base64 usado para derivar o IV na memória de forma segura>",
    "dados": "<ciphertext AES-GCM em Base64>",
    "hash_bloco": "<SHA-256 de todos os campos acima>"
  }
]
```

---

## Estrutura do usuarios.json

```json
{
  "alice": {
    "sal": "<32 bytes aleatórios em Base64 — único campo em claro>",
    "verificacao_senha": "<HMAC-SHA256 para validar a senha no login>",
    "cifrado_totp": "<segredo TOTP cifrado com AES-GCM>"
  }
}
```

> O sal é o único dado sensível armazenado em claro, conforme permitido pelo enunciado. Todo o resto é cifrado ou é um hash irreversível.
