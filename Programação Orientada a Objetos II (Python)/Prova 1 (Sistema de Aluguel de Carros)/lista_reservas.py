#classe Lista_reservas, que inicializa um dicionário que servirá como armazenamento das reservas cadastradas
class Lista_reservas:
    def __init__(self):
        self.lista_reservas = {}
    
    def get_lista_reservas(self):
        return (self.lista_reservas)