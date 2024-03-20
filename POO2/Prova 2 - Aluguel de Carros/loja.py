class Loja:
    def __init__(self):
        self.carros = []   #lista onde serão armezenados os carros cadastrados

    def adicionarCarro(self, carro):
        self.carros.append(carro)

    def listarCarros(self):
        return self.carros

    def buscarPorMarca(self, marca):
        return [carro for carro in self.carros if carro.getMarca().lower() == marca.lower()]

    def atualizarCarro(self, index, novo_carro):
        self.carros[index] = novo_carro

    def removerCarro(self, index):
        del self.carros[index]

    def calcularMediaPreco(self):
        if len(self.carros) > 0:
            total_precos = sum([float(carro.getPreco()) for carro in self.carros])
            return total_precos / len(self.carros)
        else:
            return 0.0