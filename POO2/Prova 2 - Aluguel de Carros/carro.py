class Carro:
    def __init__(self, marca, modelo, ano_fabricacao, preco, estado):
        self.marca = marca
        self.modelo = modelo
        self.ano_fabricacao = ano_fabricacao
        self.preco = preco
        self.estado = estado

    def getMarca(self):
        return self.marca

    def getModelo(self):
        return self.modelo

    def getAnoFab(self):
        return self.ano_fabricacao

    def getPreco(self):
        return self.preco

    def getEstado(self):
        return self.estado