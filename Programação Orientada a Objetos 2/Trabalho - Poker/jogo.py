class Jogo():
    def __init__(self, blind, carta_um, carta_dois, carta_tres, carta_quatro, carta_cinco):
        self.blind = blind
        self.valor_mesa = 0
        self.carta_um = carta_um
        self.carta_um_status = False
        self.carta_dois = carta_dois
        self.carta_dois_status = False
        self.carta_tres = carta_tres
        self.carta_tres_status = False
        self.carta_quatro = carta_quatro
        self.carta_quatro_status = False
        self.carta_cinco = carta_cinco
        self.carta_cinco_status = False
        
    def get_blind(self):
        return self.blind
    def get_valor_mesa(self):
        return self.valor_mesa
    def get_carta_um(self):
        return self.carta_um
    def get_carta_dois(self):
        return self.carta_dois
    def get_carta_tres(self):
        return self.carta_tres
    def get_carta_quatro(self):
        return self.carta_quatro
    def get_carta_cinco(self):
        return self.carta_cinco
    def get_carta_um_status(self):
        return self.carta_um_status
    def get_carta_dois_status(self):
        return self.carta_dois_status
    def get_carta_tres_status(self):
        return self.carta_tres_status
    def get_carta_quatro_status(self):
        return self.carta_quatro_status
    def get_carta_cinco_status(self):
        return self.carta_cinco_status
    
    def apostar(self, valor):
        self.valor_mesa += valor
    
    def virar_carta_um(self):
        self.carta_um_status = True
    def virar_carta_dois(self):
        self.carta_dois_status = True
    def virar_carta_tres(self):
        self.carta_tres_status = True
    def virar_carta_quatro(self):
        self.carta_quatro_status = True
    def virar_carta_cinco(self):
        self.carta_cinco_status = True