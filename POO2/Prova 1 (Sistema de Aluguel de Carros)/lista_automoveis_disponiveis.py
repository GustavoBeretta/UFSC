#classe Lista_automoveis_disponiveis, que inicializa um dicionário que servirá como armazenamento dos automóveis cadastrados que não estão envolvidos em nenhuma reserva, ou seja, estão disponíveis para serem alugados
class Lista_automoveis_disponiveis:
    def __init__(self):
        self.lista_automoveis_disponiveis = {}
    
    def get_lista_automoveis_disponiveis(self):
        return (self.lista_automoveis_disponiveis)