# ----------------------
# INTEGRANTES DO GRUPO
# ----------------------
# Gustavo Beretta Gonçalves
# Luana Ronau Mattos
# Rafaela Silva Borges

import sys
import string

# ----------------------
# TABELA DE SÍMBOLOS
# ----------------------

tabela_simbolos = {
    "<": "Token_relop",
    ">": "Token_relop",
    "<=": "Token_relop",
    ">=": "Token_relop",
    "!=": "Token_relop",
    "==": "Token_relop",
    "int": "Token_int",
    "if": "Token_if",
    "else": "Token_else",
    "def": "Token_def",
    "print": "Token_print",
    "return": "Token_return",
    "+": "Token_add",
    "-": "Token_sub",
    "*": "Token_mul",
    "/": "Token_div",
    "=": "Token_equal",
    "(": "Token_lparen",
    ")": "Token_rparen",
    "{": "Token_lbrace",
    "}": "Token_rbrace",
    ",": "Token_comma",
    ";": "Token_semicolon",
}

# ----------------------
# ERRO LÉXICO
# ----------------------

class LexicalError(Exception):
    pass

# ----------------------
# AFDS
# ----------------------

letras = list(string.ascii_letters)

class AfdBase:
    def __init__(self):
        self.estado = 0
        self.valido = True

    def reset(self):
        self.estado = 0
        self.valido = True


class AfdPalavra(AfdBase):
    def __init__(self):
        super().__init__()
        self.letras = set(string.ascii_letters)
        self.numeros = set(string.digits)

    def verifica_caractere(self, caractere):
        # Só pode começar com letras ou underscore
        if self.estado == 0:
            if caractere not in self.letras: 
                if caractere != "_":
                    self.valido = False
        # Outros caracteres podem ser números, letras ou underscore
        else:
            if not (caractere in self.numeros or caractere in self.letras or caractere == "_"):
                self.valido = False

        self.estado += 1


class AfdOperador(AfdBase):
    def __init__(self):
        super().__init__()
        self.operadores = {"<", ">", "=", "!", "+", "-", "*", "/", "(", ")", "{", "}", ",", ";"}

    def verifica_caractere(self, caractere):
        # Primeiro caractere pode ser qualquer um dos operadores
        if self.estado == 0:
            if caractere not in self.operadores:
                self.valido = False
        # Segundo caractere só pode ser =, válido para os símbolos >= <= != e ==
        elif self.estado == 1:
            if caractere != "=":
                self.valido = False
        # Nenhum operador pode ter mais de dois caracteres
        else:
            self.valido = False

        self.estado += 1


class AfdNumero(AfdBase):
    def __init__(self):
        super().__init__()
        self.numeros = set(string.digits)

    def verifica_caractere(self, caractere):
        if caractere not in self.numeros:
            self.valido = False

        self.estado += 1


# ----------------------
# ANALISADOR LÉXICO
# ----------------------

class AnalisadorLexico:
    def __init__(self, tabela_simbolos):
        self.tokens_saida = []
        self.tokens = []
        self.token = ""
        self.tipo_token = None
        self.tabela_simbolos = tabela_simbolos
        self.afnd_palavra = AfdPalavra()
        self.afnd_operador = AfdOperador()
        self.afnd_numero = AfdNumero()
        self.afds = [self.afnd_palavra, self.afnd_operador, self.afnd_numero]
        self.linha = 1
        self.coluna = 1

    def token_formado(self):
        self.tokens.append(self.token)

        # Se não for uma das palavras-chaves da tabela de símbolos, adiciona na tabela como identificador
        if self.token not in self.tabela_simbolos and self.tipo_token == "Palavra":
            self.tabela_simbolos[self.token] = "Token_identificador"

        tipo_final = self.tabela_simbolos.get(self.token, "ERRO")

        if self.token.isdigit(): 
            tipo_final = "Token_num"

        pacote = (tipo_final, self.token, self.linha, self.coluna)
        self.tokens_saida.append(pacote)

        # Limpa as variáveis
        self.token = ""
        self.tipo_token = None
        for afd in self.afds:
            afd.reset() # Reseta estado e validez dos AFDs

    def analise_lexica(self, codigo):
        i = 0
        while i < len(codigo):
            if codigo[i] == " " or codigo[i] == "\n" or codigo[i] == "\t" or codigo[i] == "\r":
                
                if self.token != "": 
                    self.token_formado()

                if codigo[i] == "\n":
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1

                i += 1

            else:
                if self.afnd_palavra.valido:
                    self.afnd_palavra.verifica_caractere(codigo[i])
                    if self.afnd_palavra.valido:
                        self.tipo_token = "Palavra"

                if self.afnd_operador.valido:
                    self.afnd_operador.verifica_caractere(codigo[i])
                    if self.afnd_operador.valido:
                        self.tipo_token = "Operador"

                if self.afnd_numero.valido:
                    self.afnd_numero.verifica_caractere(codigo[i])
                    if self.afnd_numero.valido:
                        self.tipo_token = "Numero"

                # Todos os AFNDs passaram do estado final
                if (self.afnd_palavra.valido == False) and (self.afnd_operador.valido == False) and (self.afnd_numero.valido == False):
                    # Se nenhum dos AFNDs reconheceu como parte da linguagem, emite erro
                    if self.tipo_token == None:
                        raise LexicalError(f"Erro léxico: caractere '{codigo[i]}' na linha '{self.linha}' "
                                           f"coluna '{self.coluna}' não pode ser reconhecido pela linguagem")
                    else:
                        self.token_formado()

                # Se ainda existem AFNDs válidos, continua no loop
                else:
                    self.token += codigo[i]
                    i += 1
                    self.coluna += 1

        # Tratamento do último caractere nos casos em que a linguagem não termina com espaço
        if self.token != "":
            self.token_formado() 
        
        # Retorna a lista para o Analisador Sintático 
        return self.tokens_saida

    def imprime_resultado(self):
        print("LISTA DE TOKENS OBTIDA:")
        # Print do primeiro item
        print(self.tabela_simbolos[self.tokens[0]], end="")
        self.tokens.pop(0)
        
        for token in self.tokens:
            if token.isdigit():
                print(f", Token_num", end="")
            else:
                print(f", {self.tabela_simbolos[token]}", end="")

        print(F"\n\nTABELA DE SÍMBOLOS AO FINAL:")
        for key, value in tabela_simbolos.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    # Para testar o léxico sozinho
    if len(sys.argv) < 2:
        print("Uso: python3 analisador_lexico.py arquivo.lsi")
    else:
        arquivo = sys.argv[1]
        with open(arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()
        
        al = AnalisadorLexico(tabela_simbolos)
        al.analise_lexica(codigo)
        al.imprime_resultado()