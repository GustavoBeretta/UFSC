# ----------------------
# INTEGRANTES DO GRUPO
# ----------------------
# Gustavo Beretta Gonçalves
# Luana Ronau Mattos
# Rafaela Silva Borges

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lexico.analisador_lexico import AnalisadorLexico, tabela_simbolos

# ---------------------------
# TABELA DE ANÁLISE SINTÁTICA 
# ---------------------------

tabela_parsing = {
    "MAIN": {
        "Token_def": ["FLIST"],
        "Token_int": ["STMT"], "Token_identificador": ["STMT"], "Token_print": ["STMT"],
        "Token_return": ["STMT"], "Token_if": ["STMT"], "Token_lbrace": ["STMT"],
        "Token_semicolon": ["STMT"],
        "$": ["ε"], "EOF": ["ε"]
    },
    "FLIST": {
        "Token_def": ["FDEF", "FLIST'"]
    },
    "FLIST'": {
        "Token_def": ["FLIST"],
        "$": ["ε"], "EOF": ["ε"]
    },
    "FDEF": {
        "Token_def": ["Token_def", "id", "Token_lparen", "PARLIST", "Token_rparen", "Token_lbrace", "STMTLIST", "Token_rbrace"]
    },
    "PARLIST": {
        "Token_int": ["Token_int", "id", "PARLIST'"],
        "Token_rparen": ["ε"]
    },
    "PARLIST'": {
        "Token_comma": ["Token_comma", "PARLIST"],
        "Token_rparen": ["ε"]
    },
    "VARLIST": {
        "id": ["id", "VARLIST'"], "Token_identificador": ["id", "VARLIST'"]
    },
    "VARLIST'": {
        "Token_comma": ["Token_comma", "VARLIST"],
        "Token_semicolon": ["ε"]
    },
    "STMT": {
        "Token_int": ["Token_int", "VARLIST", "Token_semicolon"],
        "id": ["ATRIBST", "Token_semicolon"], "Token_identificador": ["ATRIBST", "Token_semicolon"],
        "Token_print": ["Token_print", "EXPR", "Token_semicolon"],
        "Token_return": ["RETURNST", "Token_semicolon"],
        "Token_if": ["IFSTMT"],
        "Token_lbrace": ["Token_lbrace", "STMTLIST", "Token_rbrace"],
        "Token_semicolon": ["Token_semicolon"]
    },
    "STMTLIST": {
        "Token_int": ["STMT", "STMTLIST'"], "id": ["STMT", "STMTLIST'"], 
        "Token_identificador": ["STMT", "STMTLIST'"], "Token_print": ["STMT", "STMTLIST'"], 
        "Token_return": ["STMT", "STMTLIST'"], "Token_if": ["STMT", "STMTLIST'"], 
        "Token_lbrace": ["STMT", "STMTLIST'"], "Token_semicolon": ["STMT", "STMTLIST'"],
        "Token_rbrace": ["ε"]
    },
    "STMTLIST'": {
        "Token_int": ["STMTLIST"], "id": ["STMTLIST"], "Token_identificador": ["STMTLIST"],
        "Token_print": ["STMTLIST"], "Token_return": ["STMTLIST"], "Token_if": ["STMTLIST"],
        "Token_lbrace": ["STMTLIST"], "Token_semicolon": ["STMTLIST"],
        "Token_rbrace": ["ε"]
    },
    "IFSTMT": {
        "Token_if": ["Token_if", "Token_lparen", "EXPR", "Token_rparen", "Token_lbrace", "STMT", "Token_rbrace", "IF_TAIL"]
    },
    "IF_TAIL": {
        "Token_else": ["Token_else", "Token_lbrace", "STMT", "Token_rbrace"],
        "Token_int": ["ε"], "Token_print": ["ε"], "id": ["ε"], "Token_identificador": ["ε"], 
        "Token_return": ["ε"], "Token_lbrace": ["ε"], "Token_semicolon": ["ε"], 
        "Token_rbrace": ["ε"], "Token_if": ["ε"], "$": ["ε"]
    },
    "RETURNST": {
        "Token_return": ["Token_return", "RETURN_TAIL"]
    },
    "RETURN_TAIL": {
        "id": ["id"], "Token_identificador": ["id"],
        "Token_semicolon": ["ε"]
    },
    "ATRIBST": {
        "id": ["id", "Token_equal", "ATRIB_RHS"], "Token_identificador": ["id", "Token_equal", "ATRIB_RHS"]
    },
    "ATRIB_RHS": {
        "id": ["id", "ID_BRANCH"], "Token_identificador": ["id", "ID_BRANCH"],
        "num": ["num", "TERM'", "NUMEXPR'", "EXPR'"], "Token_num": ["num", "TERM'", "NUMEXPR'", "EXPR'"],
        "Token_lparen": ["Token_lparen", "NUMEXPR", "Token_rparen", "TERM'", "NUMEXPR'", "EXPR'"]
    },
    "ID_BRANCH": {
        "Token_lparen": ["Token_lparen", "PARLISTCALL", "Token_rparen"],
        "Token_semicolon": ["TERM'", "NUMEXPR'", "EXPR'"], "Token_add": ["TERM'", "NUMEXPR'", "EXPR'"],
        "Token_sub": ["TERM'", "NUMEXPR'", "EXPR'"], "Token_mul": ["TERM'", "NUMEXPR'", "EXPR'"],
        "Token_div": ["TERM'", "NUMEXPR'", "EXPR'"], "Token_relop": ["TERM'", "NUMEXPR'", "EXPR'"],
        "Token_rparen": ["TERM'", "NUMEXPR'", "EXPR'"]
    },
    "PARLISTCALL": {
        "id": ["id", "PARLISTCALL'"], "Token_identificador": ["id", "PARLISTCALL'"],
        "Token_rparen": ["ε"]
    },
    "PARLISTCALL'": {
        "Token_comma": ["Token_comma", "PARLISTCALL"],
        "Token_rparen": ["ε"]
    },
    "EXPR": {
        "num": ["NUMEXPR", "EXPR'"], "Token_num": ["NUMEXPR", "EXPR'"],
        "id": ["NUMEXPR", "EXPR'"], "Token_identificador": ["NUMEXPR", "EXPR'"],
        "Token_lparen": ["NUMEXPR", "EXPR'"]
    },
    "EXPR'": {
        "Token_relop": ["Token_relop", "NUMEXPR"],
        "Token_semicolon": ["ε"], "Token_rparen": ["ε"], "Token_comma": ["ε"]
    },
    "NUMEXPR": {
        "num": ["TERM", "NUMEXPR'"], "Token_num": ["TERM", "NUMEXPR'"],
        "id": ["TERM", "NUMEXPR'"], "Token_identificador": ["TERM", "NUMEXPR'"],
        "Token_lparen": ["TERM", "NUMEXPR'"]
    },
    "NUMEXPR'": {
        "Token_add": ["Token_add", "TERM", "NUMEXPR'"],
        "Token_sub": ["Token_sub", "TERM", "NUMEXPR'"],
        "Token_relop": ["ε"], "Token_semicolon": ["ε"], "Token_rparen": ["ε"], "Token_comma": ["ε"]
    },
    "TERM": {
        "num": ["FACTOR", "TERM'"], "Token_num": ["FACTOR", "TERM'"],
        "id": ["FACTOR", "TERM'"], "Token_identificador": ["FACTOR", "TERM'"],
        "Token_lparen": ["FACTOR", "TERM'"]
    },
    "TERM'": {
        "Token_mul": ["Token_mul", "FACTOR", "TERM'"],
        "Token_div": ["Token_div", "FACTOR", "TERM'"],
        "Token_add": ["ε"], "Token_sub": ["ε"], "Token_relop": ["ε"], 
        "Token_semicolon": ["ε"], "Token_rparen": ["ε"], "Token_comma": ["ε"]
    },
    "FACTOR": {
        "num": ["num"], "Token_num": ["num"],
        "id": ["id"], "Token_identificador": ["id"],
        "Token_lparen": ["Token_lparen", "NUMEXPR", "Token_rparen"]
    }
}

# ----------------------
# ANALISADOR SINTÁTICO
# ----------------------
class AnalisadorSintatico:
    def __init__(self, tokens, tabela):
        self.tokens = tokens
        self.tabela = tabela
        self.pilha = ["$", "MAIN"] 
        
    def erro(self, esperado, encontrado_token):
        tipo, lexema, linha, col = encontrado_token
        print(f"\n ERRO SINTÁTICO FATAL")
        print(f"Esperava: {esperado}")
        print(f"Encontrou: '{lexema}' ({tipo})")
        print(f"Local: Linha {linha}, Coluna {col}")
        sys.exit(1)

    def analisar(self):
        print("\n=== INICIANDO ANÁLISE SINTÁTICA ===\n")
        self.tokens.append(("$", "$", 0, 0)) 
        idx = 0 
        
        while len(self.pilha) > 0:
            topo = self.pilha[-1]
            token_atual = self.tokens[idx]
            tipo_token = token_atual[0]
            lexema = token_atual[1]


            # Se o topo é Epsilon (Vazio), apenas desempilha
            if topo == "ε":
                self.pilha.pop()
                continue

            # Se o topo é Terminal - Token ou $
            if topo not in self.tabela:
                # Tradutor: A tabela usa 'id' e 'num', o léxico usa 'Token_...'
                topo_traduzido = topo
                if topo == "id": topo_traduzido = "Token_identificador"
                if topo == "num": topo_traduzido = "Token_num"

                if topo_traduzido == tipo_token or topo == "$":
                    if topo == "$" and tipo_token == "$":
                        print("\n SUCESSO! Código aceito.")
                        return
                    print(f"Match: {lexema}")
                    self.pilha.pop()
                    idx += 1
                else:
                    self.erro(topo, token_atual)

            # Se o topo é Não-Terminal - Regra
            else:
                regra = None
                
                # Tenta casar exatamente o tipo do token na tabela
                if tipo_token in self.tabela[topo]:
                    regra = self.tabela[topo][tipo_token]
                # Tenta casar os genéricos (id ou num)
                elif "id" in self.tabela[topo] and tipo_token == "Token_identificador":
                    regra = self.tabela[topo]["id"]
                elif "num" in self.tabela[topo] and tipo_token == "Token_num":
                    regra = self.tabela[topo]["num"]
                
                if regra:
                    print(f"Regra: {topo} -> {regra}")
                    self.pilha.pop()
                    if regra != ["ε"]:
                        # Empilha ao contrário
                        for simbolo in reversed(regra):
                            self.pilha.append(simbolo)
                else:
                    self.erro(f"Regra válida para {topo} com token {tipo_token}", token_atual)

# ---------------------
# EXECUÇÃO PRINCIPAL
# ---------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 analisador_sintatico.py <arquivo.lsi>")
    else:
        arquivo = sys.argv[1]
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                codigo = f.read()

            print("--- Executando Léxico ---")
            lexico = AnalisadorLexico(tabela_simbolos)
            tokens = lexico.analise_lexica(codigo)
            
            print("--- Executando Sintático ---")
            sintatico = AnalisadorSintatico(tokens, tabela_parsing)
            sintatico.analisar()

        except Exception as e:
            print(f"Erro: {e}")