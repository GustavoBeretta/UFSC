from carro import Carro
import tkinter as tk
from tkinter import messagebox
import json

class LojaGUI:
    def __init__(self, loja):
        self.loja = loja
        self.window = tk.Tk()
        self.window.title("Sistema de Gerenciamento do Estoque de Carros")

        label_marca = tk.Label(self.window, text="Marca:")
        label_marca.grid(row=0, column=0)
        label_modelo = tk.Label(self.window, text="Modelo:")
        label_modelo.grid(row=1, column=0)
        label_ano = tk.Label(self.window, text="Ano de Fabricação:", width=16)
        label_ano.grid(row=2, column=0)
        label_preco = tk.Label(self.window, text="Preço:")
        label_preco.grid(row=3, column=0)
        label_estado = tk.Label(self.window, text="Estado:")
        label_estado.grid(row=4, column=0)
        
        self.var_estado = tk.StringVar(value='Nada')
        
        self.entry_marca = tk.Entry(self.window)
        self.entry_marca.grid(row=0, column=1, columnspan=2)
        self.entry_modelo = tk.Entry(self.window)
        self.entry_modelo.grid(row=1, column=1, columnspan=2)
        self.entry_ano = tk.Entry(self.window)
        self.entry_ano.grid(row=2, column=1, columnspan=2)
        self.entry_preco = tk.Entry(self.window)
        self.entry_preco.grid(row=3, column=1, columnspan=2)
        self.entry_novo = tk.Radiobutton(text='Novo', variable=self.var_estado, value='Novo')
        self.entry_novo.grid(row=4, column=1)
        self.entry_usado = tk.Radiobutton(text='Usado', variable=self.var_estado, value='Usado')
        self.entry_usado.grid(row=4, column=2)

        button_adicionar = tk.Button(self.window, text="Adicionar Carro", command=self.adicionar_carro)
        button_adicionar.grid(row=5, column=0)
        button_listar = tk.Button(self.window, text="Listar Carros", command=self.listar_carros)
        button_listar.grid(row=5, column=1)
        button_buscar = tk.Button(self.window, text="Buscar pela Marca", command=self.buscar_por_marca)
        button_buscar.grid(row=6, column=0)
        button_atualizar = tk.Button(self.window, text="Atualizar Carro", command=self.atualizar_carro)
        button_atualizar.grid(row=6, column=1)
        button_remover = tk.Button(self.window, text="Remover Carro", command=self.remover_carro)
        button_remover.grid(row=7, column=0)
        button_media = tk.Button(self.window, text="Média de Preço", command=self.calcular_media_preco)
        button_media.grid(row=7, column=1)

        self.listbox_resultado = tk.Listbox(self.window, width=38)
        self.listbox_resultado.grid(row=8, columnspan=3)

    def adicionar_carro(self):
        erro = 0
        if self.entry_marca.get() != '':
            marca = self.entry_marca.get().strip()
        else:
            erro += 1
        if self.entry_modelo.get() != '':
            modelo = self.entry_modelo.get().strip()
        else:
            erro += 1
        if self.entry_ano.get().isnumeric():
            ano = self.entry_ano.get()
        else:
            erro += 1
        if self.entry_preco.get().isnumeric() and self.entry_preco.get() != '0':
            preco = self.entry_preco.get()
        else:
            erro += 1
        if self.var_estado.get() != 'Nada':
            estado = self.var_estado.get()
        else:
            erro += 1
        
        if erro == 0:
            carro = Carro(marca, modelo, ano, preco, estado)
            self.loja.adicionarCarro(carro)
            self.salvar_dados()
            messagebox.showinfo("Sucesso", "Carro adicionado com sucesso!")
        else:
            messagebox.showerror("ERRO", "Um ou mais campos não foram preenchidos corretamente! Tente novamente.")

    def listar_carros(self):
        self.listbox_resultado.delete(0, tk.END)
        carros = self.loja.listarCarros()
        for carro in carros:
            info_carro = f"{carro.getMarca()} \n" \
                         f"{carro.getModelo()} \n" \
                         f"{carro.getAnoFab()} \n" \
                         f"{carro.getEstado()} \n" \
                         f"R${carro.getPreco()}"
            self.listbox_resultado.insert(tk.END, info_carro)

    def buscar_por_marca(self):
        self.listbox_resultado.delete(0, tk.END)
        marca = self.entry_marca.get()
        carros = self.loja.buscarPorMarca(marca)
        for carro in carros:
            info_carro = f"{carro.getMarca()} \n" \
                         f"{carro.getModelo()} \n" \
                         f"{carro.getAnoFab()} \n" \
                         f"{carro.getEstado()} \n" \
                         f"R${carro.getPreco()}"
            self.listbox_resultado.insert(tk.END, info_carro)

    def atualizar_carro(self):
        index = self.listbox_resultado.curselection()
        if index:
            erro = 0
            if self.entry_marca.get() != '':
                marca = self.entry_marca.get().strip()
            else:
                erro += 1
            if self.entry_modelo.get() != '':
                modelo = self.entry_modelo.get().strip()
            else:
                erro += 1
            if self.entry_ano.get().isnumeric():
                ano = self.entry_ano.get()
            else:
                erro += 1
            if self.entry_preco.get().isnumeric() and self.entry_preco.get() != '0':
                preco = self.entry_preco.get()
            else:
                erro += 1
            if self.var_estado.get() != 'Nada':
                estado = self.var_estado.get()
            else:
                erro += 1
            
            if erro == 0:
                carro = Carro(marca, modelo, ano, preco, estado)
                self.loja.atualizarCarro(index[0], carro)
                self.salvar_dados()
                messagebox.showinfo("Sucesso", "Carro atualizado com sucesso!")
                self.listbox_resultado.delete(0, tk.END)
                carros = self.loja.listarCarros()
                for carro in carros:
                    info_carro = f"{carro.getMarca()} \n" \
                                 f"{carro.getModelo()} \n" \
                                 f"{carro.getAnoFab()} \n" \
                                 f"{carro.getEstado()} \n" \
                                 f"R${carro.getPreco()}"
                    self.listbox_resultado.insert(tk.END, info_carro)
            else:
                messagebox.showerror("ERRO", "Um ou mais campos não foram preenchidos corretamente! Tente novamente.") 
        else:
            messagebox.showerror("ERRO", "Nenhum carro selecionado.")

    def remover_carro(self):
        index = self.listbox_resultado.curselection()
        if index:
            self.loja.removerCarro(index[0])
            self.salvar_dados()
            messagebox.showinfo("Sucesso", "Carro removido com sucesso!")
            self.listbox_resultado.delete(0, tk.END)
            carros = self.loja.listarCarros()
            for carro in carros:
                info_carro = f"{carro.getMarca()} \n" \
                             f"{carro.getModelo()} \n" \
                             f"{carro.getAnoFab()} \n" \
                             f"{carro.getEstado()} \n" \
                             f"R${carro.getPreco()}"
                self.listbox_resultado.insert(tk.END, info_carro)
        else:
            messagebox.showerror("ERRO", "Nenhum carro selecionado.")

    def calcular_media_preco(self):
        media = self.loja.calcularMediaPreco()
        messagebox.showinfo("Média de Preço", f"A média de preço dos carros cadastrados é: R${media:.2f}")

    def salvar_dados(self):
        dados=[]
        for carro in self.loja.listarCarros():
            carro_data = {
                "marca": carro.getMarca(),
                "modelo": carro.getModelo(),
                "ano_fabricacao": carro.getAnoFab(),
                "preco": carro.getPreco(),
                "estado": carro.getEstado()
            }
            dados.append(carro_data)

        with open("estoque_carros.json", "w") as arquivo:
            json.dump(dados, arquivo)
            
    def carregar_dados(self):
        try:
            with open("estoque_carros.json", "r") as arquivo:
                dados = json.load(arquivo)

            for carro_data in dados:
                marca = carro_data["marca"]
                modelo = carro_data["modelo"]
                ano_fabricacao = carro_data["ano_fabricacao"]
                preco = carro_data["preco"]
                estado = carro_data["estado"]
                carro = Carro(marca, modelo, ano_fabricacao, preco, estado)
                self.loja.adicionarCarro(carro)

        except FileNotFoundError:
            pass

    def run(self):
        self.carregar_dados()
        self.window.mainloop()