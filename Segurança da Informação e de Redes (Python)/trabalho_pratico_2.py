"""
Mini-Blockchain Simétrica com Autenticação de Usuário
INE 5680 / INE410148 - Segurança da Informação e de Redes
UFSC - Departamento de Informática e Estatística

Funcionalidades:
- Cadastro e login com senha + TOTP (2FA)
- Derivação de chave com PBKDF2
- Criptografia AES-GCM por bloco
- Blockchain encadeada com hash_anterior
- Sistema multiusuário
"""

import os
import json
import hashlib
import hmac
import struct
import time
import base64
import secrets
import getpass
from datetime import datetime
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

ARQUIVO_USUARIOS    = "usuarios.json"
ARQUIVO_BLOCKCHAIN  = "blockchain.json"

def derivar_chave(senha: str, sal: bytes, iteracoes: int = 600_000, tamanho_chave: int = 32) -> bytes:
    funcao_derivacao = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=tamanho_chave,
        salt=sal,
        iterations=iteracoes,
        backend=default_backend()
    )
    return funcao_derivacao.derive(senha.encode("utf-8"))


def derivar_chave_sessao(chave_mestra: bytes, contexto: bytes) -> bytes:
    return hmac.new(chave_mestra, b"chave_sessao|" + contexto, hashlib.sha256).digest()


def derivar_chave_e_iv(chave_mestra: bytes, sal: bytes, iteracoes: int = 200_000) -> tuple[bytes, bytes]:

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=44,
        salt=sal,
        iterations=iteracoes,
        backend=default_backend(),
    )
    mater = kdf.derive(chave_mestra)
    return mater[:32], mater[32:44]




def cifrar_aes_gcm(chave: bytes, texto_claro: bytes) -> tuple[bytes, bytes]:
    vetor_inicializacao = secrets.token_bytes(12)   # 96 bits – tamanho recomendado para GCM
    aesgcm = AESGCM(chave)
    texto_cifrado = aesgcm.encrypt(vetor_inicializacao, texto_claro, None)
    return vetor_inicializacao, texto_cifrado


def decifrar_aes_gcm(chave: bytes, vetor_inicializacao: bytes, texto_cifrado: bytes) -> bytes:
    aesgcm = AESGCM(chave)
    return aesgcm.decrypt(vetor_inicializacao, texto_cifrado, None)




def gerar_segredo_totp() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode("utf-8")


def _calcular_hotp(chave_b32: str, contador: int) -> int:
    chave_bytes = base64.b32decode(chave_b32, casefold=True)
    mensagem = struct.pack(">Q", contador)          # contador de 8 bytes big-endian
    digest = hmac.new(chave_bytes, mensagem, hashlib.sha1).digest()
    deslocamento = digest[-1] & 0x0F
    codigo = struct.unpack(">I", digest[deslocamento:deslocamento + 4])[0] & 0x7FFFFFFF
    return codigo % 1_000_000


def calcular_totp(segredo_b32: str, janela: int = 0) -> str:
    epoca = int(time.time()) // 30 + janela
    return f"{_calcular_hotp(segredo_b32, epoca):06d}"


def verificar_totp(segredo_b32: str, codigo: str) -> bool:
    for janela in (-1, 0, 1):
        if calcular_totp(segredo_b32, janela) == codigo.strip():
            return True
    return False

def calcular_hash_bloco(bloco: dict) -> str:
    dados = {chave: valor for chave, valor in bloco.items() if chave != "hash_bloco"}
    serializado = json.dumps(dados, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serializado.encode("utf-8")).hexdigest()


def carregar_blockchain() -> list:
    if not os.path.exists(ARQUIVO_BLOCKCHAIN):
        return []
    with open(ARQUIVO_BLOCKCHAIN, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_blockchain(cadeia: list) -> None:
    with open(ARQUIVO_BLOCKCHAIN, "w", encoding="utf-8") as arquivo:
        json.dump(cadeia, arquivo, indent=2, ensure_ascii=False)


def carregar_usuarios() -> dict:
    if not os.path.exists(ARQUIVO_USUARIOS):
        return {}
    with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_usuarios(usuarios: dict) -> None:
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=2, ensure_ascii=False)




def cifrar_segredo_totp(chave_mestra: bytes, segredo_totp: str) -> tuple[str, str]:
    iv = secrets.token_bytes(12)
    aesgcm = AESGCM(chave_mestra)
    texto_cifrado = aesgcm.encrypt(iv, segredo_totp.encode("utf-8"), None)
    combinado = iv + texto_cifrado
    return base64.b64encode(combinado).decode()


def decifrar_segredo_totp(chave_mestra: bytes, registro: dict) -> str:
    blob_b64 = registro.get("cifrado_totp")
    vi_b64 = registro.get("vi_totp")

    if blob_b64 and not vi_b64:
        combinado = base64.b64decode(blob_b64)
        iv = combinado[:12]
        texto_cifrado = combinado[12:]
        return decifrar_aes_gcm(chave_mestra, iv, texto_cifrado).decode("utf-8")

    if vi_b64 and blob_b64:
        iv = base64.b64decode(vi_b64)
        texto_cifrado = base64.b64decode(blob_b64)
        return decifrar_aes_gcm(chave_mestra, iv, texto_cifrado).decode("utf-8")

    raise ValueError("Registro TOTP inválido ou incompleto")

def cadastrar_usuario() -> None:
    usuarios = carregar_usuarios()

    print("\n=== CADASTRO DE USUÁRIO ===")
    nome_usuario = input("Nome de usuário: ").strip()
    if not nome_usuario:
        print("[ERRO] Nome de usuário não pode ser vazio.")
        return
    if nome_usuario in usuarios:
        print(f"[ERRO] Usuário '{nome_usuario}' já existe.")
        return

    senha    = getpass.getpass("Senha: ")
    confirma = getpass.getpass("Confirme a senha: ")
    if senha != confirma:
        print("[ERRO] As senhas não coincidem.")
        return
    if len(senha) < 8:
        print("[ERRO] Senha deve ter pelo menos 8 caracteres.")
        return

    sal = secrets.token_bytes(32)

    chave_mestra = derivar_chave(senha, sal)

    verificacao_senha = hmac.new(
        chave_mestra, b"token_verificacao_senha", hashlib.sha256
    ).hexdigest()

    
    segredo_totp = gerar_segredo_totp()

    cifrado_totp = cifrar_segredo_totp(chave_mestra, segredo_totp)

    usuarios[nome_usuario] = {
        "sal":               base64.b64encode(sal).decode(),
        "verificacao_senha": verificacao_senha,
        "cifrado_totp":      cifrado_totp,
    }
    salvar_usuarios(usuarios)

    print(f"\n[OK] Usuário '{nome_usuario}' cadastrado com sucesso!")
    print(f"\n[TOTP] Configure seu autenticador (Google Authenticator, Authy, etc.)")
    print(f"       Chave secreta TOTP (Base32): {segredo_totp}")
    print(f"       Código atual para teste:     {calcular_totp(segredo_totp)}")
    print(f"\n[ATENÇÃO] Guarde a chave TOTP – ela não será exibida novamente.\n")


def fazer_login() -> tuple[str | None, bytes | None]:
    usuarios = carregar_usuarios()

    print("\n=== LOGIN ===")
    nome_usuario = input("Nome de usuário: ").strip()
    if nome_usuario not in usuarios:
        print("[ERRO] Usuário não encontrado.")
        return None, None

    senha = getpass.getpass("Senha: ")

    registro     = usuarios[nome_usuario]
    sal          = base64.b64decode(registro["sal"])
    chave_mestra = derivar_chave(senha, sal)

    verificacao_esperada = hmac.new(
        chave_mestra, b"token_verificacao_senha", hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(verificacao_esperada, registro["verificacao_senha"]):
        print("[ERRO] Senha incorreta.")
        return None, None

    try:
        segredo_totp = decifrar_segredo_totp(chave_mestra, registro)
    except Exception:
        print("[ERRO] Falha ao decifrar segredo TOTP – dados corrompidos.")
        return None, None

    codigo_totp = input("Código TOTP (6 dígitos): ").strip()
    if not verificar_totp(segredo_totp, codigo_totp):
        print("[ERRO] Código TOTP inválido ou expirado.")
        return None, None

    chave_sessao = derivar_chave_sessao(chave_mestra, b"sessao_blockchain")
    print(f"\n[OK] Login bem-sucedido. Bem-vindo, {nome_usuario}!\n")
    return nome_usuario, chave_sessao


def adicionar_bloco(nome_usuario: str, chave_mestra: bytes) -> None:
    cadeia = carregar_blockchain()

    print("\n=== ADICIONAR BLOCO ===")
    dados = input("Dados do bloco (transação/mensagem): ").strip()
    if not dados:
        print("[ERRO] Dados não podem ser vazios.")
        return

    if cadeia:
        ultimo_bloco    = cadeia[-1]
        hash_esperado   = calcular_hash_bloco(ultimo_bloco)
        if not hmac.compare_digest(hash_esperado, ultimo_bloco.get("hash_bloco", "")):
            print("[ERRO] Integridade da blockchain comprometida! Operação abortada.")
            return
        hash_anterior = ultimo_bloco["hash_bloco"]
    else:
        hash_anterior = "0" * 64   # bloco gênese

    sal_bloco = secrets.token_bytes(16)
    chave_bloco, iv_bloco = derivar_chave_e_iv(chave_mestra, sal_bloco)

    texto_claro = dados.encode("utf-8")
    aesgcm = AESGCM(chave_bloco)
    texto_cifrado = aesgcm.encrypt(iv_bloco, texto_claro, None)

    novo_bloco = {
        "indice":         len(cadeia),
        "proprietario":   nome_usuario,
        "timestamp":      datetime.utcnow().isoformat() + "Z",
        "hash_anterior":  hash_anterior,
        "sal_bloco":      base64.b64encode(sal_bloco).decode(),
        "dados":          base64.b64encode(texto_cifrado).decode(),
    }
    novo_bloco["hash_bloco"] = calcular_hash_bloco(novo_bloco)

    cadeia.append(novo_bloco)
    salvar_blockchain(cadeia)

    print(f"[OK] Bloco #{novo_bloco['indice']} adicionado à blockchain.")
    print(f"     Hash: {novo_bloco['hash_bloco'][:32]}...")


def ler_blockchain(nome_usuario: str, chave_mestra: bytes) -> None:
    cadeia = carregar_blockchain()

    if not cadeia:
        print("\n[INFO] Blockchain vazia.")
        return

    print(f"\n=== BLOCKCHAIN ({len(cadeia)} blocos) ===\n")

    hash_anterior_verificado = "0" * 64
    cadeia_integra = True

    for bloco in cadeia:
        indice         = bloco["indice"]
        proprietario   = bloco["proprietario"]
        timestamp      = bloco["timestamp"]
        hash_anterior  = bloco["hash_anterior"]
        hash_armazenado = bloco.get("hash_bloco", "")

        encadeamento_ok = hmac.compare_digest(hash_anterior, hash_anterior_verificado)
        bloco_ok        = hmac.compare_digest(calcular_hash_bloco(bloco), hash_armazenado)

        if not encadeamento_ok or not bloco_ok:
            cadeia_integra = False
            rotulo_integridade = "X COMPROMETIDO"
        else:
            rotulo_integridade = "✓ OK"

        print(f"Bloco #{indice}")
        print(f"  Proprietário : {proprietario}")
        print(f"  Timestamp    : {timestamp}")
        print(f"  Hash         : {hash_armazenado[:32]}...")
        print(f"  Hash Anterior: {hash_anterior[:32]}...")
        print(f"  Integridade  : {rotulo_integridade}")

        if proprietario == nome_usuario:
            try:
                if "sal_bloco" in bloco:
                    sal_bloco = base64.b64decode(bloco["sal_bloco"])
                    chave_bloco, iv_bloco = derivar_chave_e_iv(chave_mestra, sal_bloco)
                    texto_cifrado = base64.b64decode(bloco["dados"])
                    aesgcm = AESGCM(chave_bloco)
                    texto_claro = aesgcm.decrypt(iv_bloco, texto_cifrado, None)
                    print(f"  Dados        : {texto_claro.decode('utf-8')}")
                elif "vi" in bloco:
                    vi = base64.b64decode(bloco["vi"])
                    texto_cifrado = base64.b64decode(bloco["dados"])
                    texto_claro = decifrar_aes_gcm(chave_mestra, vi, texto_cifrado)
                    print(f"  Dados        : {texto_claro.decode('utf-8')}")
                else:
                    print("  Dados        : formato de bloco desconhecido")
            except Exception:
                print("  Dados        : [ERRO de decifragem – dados adulterados ou chave diferente]")
        else:
            print("  Dados        : cifrado (acesso negado)")

        print()
        hash_anterior_verificado = hash_armazenado

    if not cadeia_integra:
        print("Aviso: integridade da blockchain comprometida.")
    else:
        print("Cadeia íntegra. Todos os hashes são válidos.")


def validar_cadeia() -> None:
    cadeia = carregar_blockchain()
    if not cadeia:
        print("\n[INFO] Blockchain vazia.")
        return

    hash_anterior_verificado = "0" * 64
    cadeia_integra = True

    print(f"\n=== VALIDAÇÃO DA CADEIA ({len(cadeia)} blocos) ===\n")
    for bloco in cadeia:
        hash_armazenado  = bloco.get("hash_bloco", "")
        hash_calculado   = calcular_hash_bloco(bloco)
        encadeamento_ok  = hmac.compare_digest(bloco["hash_anterior"], hash_anterior_verificado)
        hash_proprio_ok  = hmac.compare_digest(hash_armazenado, hash_calculado)

        simbolo = "✓" if (encadeamento_ok and hash_proprio_ok) else "X"
        print(f"  Bloco #{bloco['indice']} [{bloco['proprietario']}] {simbolo}")

        if not (encadeamento_ok and hash_proprio_ok):
            cadeia_integra = False
            if not encadeamento_ok:
                print("    → hash_anterior não bate com hash do bloco anterior!")
            if not hash_proprio_ok:
                print("    → hash do próprio bloco foi alterado!")

        hash_anterior_verificado = hash_armazenado

    print()
    if cadeia_integra:
        print("[OK] Blockchain íntegra.")
    else:
        print("[ERRO] Blockchain COMPROMETIDA – adulteração detectada!")

def menu_autenticado(nome_usuario: str, chave_mestra: bytes) -> None:
    while True:
        print(f"\n=== MENU [{nome_usuario}] ===")
        print("  1. Adicionar bloco")
        print("  2. Listar blockchain (com decifragem dos meus blocos)")
        print("  3. Validar integridade da cadeia")
        print("  4. Logout")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            adicionar_bloco(nome_usuario, chave_mestra)
        elif opcao == "2":
            ler_blockchain(nome_usuario, chave_mestra)
        elif opcao == "3":
            validar_cadeia()
        elif opcao == "4":
            print(f"\n[OK] Logout de '{nome_usuario}'.\n")
            break
        else:
            print("[ERRO] Opção inválida.")


def principal() -> None:
    print("Mini-Blockchain - Autenticação de Usuário")
    print("INE 5680 - UFSC | PBKDF2 + AES-GCM + TOTP")

    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("  1. Cadastrar usuário")
        print("  2. Login")
        print("  3. Validar integridade da blockchain (sem login)")
        print("  4. Sair")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            nome_usuario, chave_mestra = fazer_login()
            if nome_usuario and chave_mestra:
                menu_autenticado(nome_usuario, chave_mestra)
        elif opcao == "3":
            validar_cadeia()
        elif opcao == "4":
            print("\nEncerrando. Até logo!\n")
            break
        else:
            print("[ERRO] Opção inválida.")


if __name__ == "__main__":
    principal()