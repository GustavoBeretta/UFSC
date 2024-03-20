class Jogador():
    def __init__(self, nome, fichas, carta_um, carta_dois):
        self.status = True
        self.nome = nome
        self.fichas = fichas
        self.aposta = 0
        self.funcao = 'Nada'
        self.carta_um = carta_um
        self.carta_dois = carta_dois
    
    def get_status(self):
        return self.status
    def get_nome(self):
        return self.nome
    def get_fichas(self):
        return self.fichas
    def get_aposta(self):
        return self.aposta
    def get_funcao(self):
        return self.funcao  
    def get_carta_um(self):
        return self.carta_um
    def get_carta_dois(self):
        return self.carta_dois
    
    def set_funcao(self, funcao):
        self.funcao = funcao
    def set_carta_um(self, carta_um):
        self.carta_um = carta_um
    def set_carta_dois(self, carta_dois):
        self.carta_dois = carta_dois
    
    def sair(self):
        self.status = False
    
    def entrar(self):
        self.status = True
    
    def apostar(self, valor):
        self.aposta += valor
        self.fichas = self.fichas - valor
    
    def zerar_aposta(self):
        self.aposta = 0
    
    def ganhar(self, valor):
        self.fichas += valor