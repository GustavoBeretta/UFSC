#classe Lista_automoveis, que inicializa um dicionário que servirá como armazenamento dos automóveis cadastrados
class Lista_automoveis:
    def __init__(self):
        self.lista_automoveis = {}
    
    def get_lista_automoveis(self):
        return (self.lista_automoveis)