#import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conexao = sqlite3.connect('dados.db')
cursor = conexao.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS pecas (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT NOT NULL, tamanho TEXT NOT NULL, cor TEXT NOT NULL, valor TEXT NOT NULL)')
conexao.commit()

login = ctk.CTk()
login.title('Login do Sistema')

login.geometry("300x80")

login.eval('tk::PlaceWindow . center')
login.grid_rowconfigure(0, weight=1)
login.grid_columnconfigure(0, weight=1)



mensagem_tela_login = ctk.CTkLabel(master=login, text='TELA DE LOGIN', height=10)
mensagem_tela_login.grid(row=0, columnspan=2)

mensagem_senha = ctk.CTkLabel(master=login, text='SENHA: ', height=2, width=9)
mensagem_senha.grid(row=1, column=0)
senha = ctk.CTkEntry(master=login)
senha.grid(row=1, column=1)

def fazer_login():
    
    if senha.get() == '123':
        
        login.destroy()
        
        menu_principal = ctk.CTk()
        menu_principal.title('Menu Principal')
        menu_principal.geometry("200x150")

        menu_principal.eval('tk::PlaceWindow . center')
        menu_principal.grid_rowconfigure(0, weight=1)
        menu_principal.grid_columnconfigure(0, weight=1)
        
        mensagem_menu_principal = ctk.CTkLabel(master=menu_principal, text='MENU PRINCIPAL', width=30, height=2)
        mensagem_menu_principal.grid(row=0)
        
        def cadastrar_nova_peca():
            
            tela_cadastro = ctk.CTkToplevel()
            tela_cadastro.title('Cadastrar Nova Peça')
            
            tipos = ['Calçado','Calça','Short','Camiseta','Casaco']
            mensagem_tipo = ctk.CTkLabel(tela_cadastro, text='Tipo da Peça: ', height=2)
            mensagem_tipo.grid(row=0, column=0)
            tipo = ttk.Combobox(tela_cadastro, values=tipos)
            tipo.grid(row=0, column=1)
            
            mensagem_tamanho = ctk.CTkLabel(tela_cadastro, text='Tamanho da Peça: ', width=20, height=2)
            mensagem_tamanho.grid(row=1, column=0)
            tamanho = ctk.CTkEntry(tela_cadastro, width=73)
            tamanho.grid(row=1, column=1)
            
            mensagem_cor = ctk.CTkLabel(tela_cadastro, text='Cor da Peça: ', height=2)
            mensagem_cor.grid(row=2, column=0)
            cor = ctk.CTkEntry(tela_cadastro, width=73)
            cor.grid(row=2, column=1)
            
            mensagem_valor = ctk.CTkLabel(tela_cadastro, text='Valor da Peça: ', height=2)
            mensagem_valor.grid(row=3, column=0)
            valor = ctk.CTkEntry(tela_cadastro, width=73)
            valor.grid(row=3, column=1)
            
            def cadastro_voltar():
                tela_cadastro.destroy()
                
            botao_cadastro_voltar = ctk.CTkButton(tela_cadastro, text='Voltar', width=9, command=cadastro_voltar)
            botao_cadastro_voltar.grid(row=4, column=0)
            
            def cadastrar():
                
                cadastro = ctk.CTkToplevel()
                cadastro.title('Cadastro')
                erros = 0
                
                if tipo.get() == '':
                    erro_tipo = ctk.CTkLabel(cadastro, text='Um tipo de peça deve ser selecionado', width=50, height=2)
                    erro_tipo.grid()
                    erros += 1
                
                if tamanho.get() == '':
                    erro_tamanho = ctk.CTkLabel(cadastro, text='Um tamanho deve ser preenchido', width=50, height=2)
                    erro_tamanho.grid()
                    erros += 1
                
                if not cor.get().isalpha():
                    erro_cor = ctk.CTkLabel(cadastro, text='A cor deve ser uma palavra', width=50, height=2)
                    erro_cor.grid()
                    erros += 1
                
                if (not valor.get().isnumeric()) or valor.get() == '0':
                    erro_valor = ctk.CTkLabel(cadastro, text='O valor da peça deve ser um número positivo', width=50, height=2)
                    erro_valor.grid()
                    erros += 1
                    
                if erros == 0:
                    
                    cursor.execute('INSERT INTO pecas (tipo, tamanho, cor, valor) VALUES (?, ?, ?, ?)', (tipo.get(), tamanho.get(), cor.get(), valor.get()))
                    conexao.commit()
                    
                    cadastrada = ctk.CTkLabel(cadastro, text='A peça foi cadastrada', width=25, height=2)
                    cadastrada.grid()
                    
                    def ok():
                        cadastro.destroy()
                        tela_cadastro.destroy()
                    
                    botao_ok = ctk.CTkButton(cadastro, text='OK', command=ok)
                    botao_ok.grid()
                
                else:
                
                    def ok():
                        cadastro.destroy()

                    botao_ok = ctk.CTkButton(cadastro, text='OK', command=ok)
                    botao_ok.grid()

                cadastro.mainloop()
                
                tela_cadastro.destroy()
            
            botao_cadastrar = ctk.CTkButton(tela_cadastro, text='Cadastrar', command=cadastrar)
            botao_cadastrar.grid(row=4, column=1,)
            
            tela_cadastro.mainloop()
        
        botao_cadastrar_peca = ctk.CTkButton(menu_principal, text='Cadastrar Nova Peça', command=cadastrar_nova_peca, width=25)
        botao_cadastrar_peca.grid(row=1)
        
        def excluir_uma_peca():
            
            tela_exclusao = ctk.CTkToplevel()
            tela_exclusao.title('Excluir Uma Peça')
            
            mensagem_id_exclusao = ctk.CTkLabel(tela_exclusao, text='ID da peça a ser excluída: ', width=22, height=2)
            mensagem_id_exclusao.grid(row=0, column=0)
            id_exclusao = ctk.CTkEntry(tela_exclusao, width=4)
            id_exclusao.grid(row=0, column=1)
            
            def exclusao_voltar():
                tela_exclusao.destroy()
            
            botao_exclusao_voltar = ctk.CTkButton(tela_exclusao, text='Voltar', command=exclusao_voltar)
            botao_exclusao_voltar.grid(row=1, column=0)
            
            def excluir():
                
                if (not id_exclusao.get().isnumeric()) or id_exclusao.get() == '0':
                    messagebox.showinfo('Exclusão', 'O ID da peça deve ser um número positivo')
                    
                else:
                
                    cursor.execute('DELETE FROM pecas WHERE id = ?', (id_exclusao.get()))
                    conexao.commit()
                    
                    messagebox.showinfo('Exclusão', 'A peça foi excluída')
                    
                    tela_exclusao.destroy()
            
            botao_excluir = ctk.CTkButton(tela_exclusao, text='Excluir', command=excluir)
            botao_excluir.grid(row=1, column=1,)
            
            tela_exclusao.mainloop()
        
        botao_excluir_peca = ctk.CTkButton(menu_principal, text='Excluir Uma Peça', command=excluir_uma_peca, width=25)
        botao_excluir_peca.grid(row=2)
        
        def consultar_pecas():
            
            cursor.execute('SELECT * FROM pecas')
            pecas = cursor.fetchall()
            
            messagebox.showinfo('Peças', str(pecas))
        
        botao_consultar_pecas = ctk.CTkButton(menu_principal, text='Consultar Peças', command=consultar_pecas, width=25)
        botao_consultar_pecas.grid(row=3)
        
        def atualizar_peca():
            
            tela_atualizacao = ctk.CTkToplevel()
            tela_atualizacao.title('Atualizar Uma Peça')
            
            mensagem_n_id = ctk.CTkLabel(tela_atualizacao, text='ID da peça a ser atualizada: ', width=22, height=2)
            mensagem_n_id.grid(row=0, column=0)
            n_id = ctk.CTkEntry(tela_atualizacao, width=73)
            n_id.grid(row=0, column=1)
            
            tipos = ['Calçado','Calça','Short','Camiseta','Casaco']
            mensagem_tipo = ctk.CTkLabel(tela_atualizacao, text='Tipo da Peça: ', height=2)
            mensagem_tipo.grid(row=1, column=0)
            tipo = ttk.Combobox(tela_atualizacao, values=tipos)
            tipo.grid(row=1, column=1)
                    
            mensagem_tamanho = ctk.CTkLabel(tela_atualizacao, text='Tamanho da Peça: ', height=2)
            mensagem_tamanho.grid(row=2, column=0)
            tamanho = ctk.CTkEntry(tela_atualizacao, width=73)
            tamanho.grid(row=2, column=1)
                    
            mensagem_cor = ctk.CTkLabel(tela_atualizacao, text='Cor da Peça: ', height=2)
            mensagem_cor.grid(row=3, column=0)
            cor = ctk.CTkEntry(tela_atualizacao, width=73)
            cor.grid(row=3, column=1)
                    
            mensagem_valor = ctk.CTkLabel(tela_atualizacao, text='Valor da Peça: ', height=2)
            mensagem_valor.grid(row=4, column=0)
            valor = ctk.CTkEntry(tela_atualizacao, width=73)
            valor.grid(row=4, column=1)
                    
            def atualizacao_voltar():
                tela_atualizacao.destroy()
                        
            botao_atualizacao_voltar = ctk.CTkButton(tela_atualizacao, text='Voltar', width=9, command=atualizacao_voltar)
            botao_atualizacao_voltar.grid(row=5, column=0)
                    
            def atualizar():
                        
                atualizacao = ctk.CTkToplevel()
                atualizacao.title('Atualização')
                erros = 0
                
                if (not n_id.get().isnumeric()) or n_id.get() == '0':
                    erro_id = ctk.CTkLabel(atualizacao, text='O ID da peça deve ser um número positivo', width=50, height=2)
                    erro_id.grid()
                    erros += 1
                
                if tipo.get() == '':
                    erro_tipo = ctk.CTkLabel(atualizacao, text='Um tipo de peça deve ser selecionado', width=50, height=2)
                    erro_tipo.grid()
                    erros += 1
                        
                if tamanho.get() == '':
                    erro_tamanho = ctk.CTkLabel(atualizacao, text='Um tamanho deve ser preenchido', width=50, height=2)
                    erro_tamanho.grid()
                    erros += 1
                        
                if not cor.get().isalpha():
                    erro_cor = ctk.CTkLabel(atualizacao, text='A cor deve ser uma palavra', width=50, height=2)
                    erro_cor.grid()
                    erros += 1
                        
                if (not valor.get().isnumeric()) or valor.get() == '0':
                    erro_valor = ctk.CTkLabel(atualizacao, text='O valor da peça deve ser um número positivo', width=50, height=2)
                    erro_valor.grid()
                    erros += 1
                            
                if erros == 0:
                            
                    cursor.execute('UPDATE pecas SET tipo = ?, tamanho = ?, cor = ?, valor = ? WHERE id = ?', (tipo.get(), tamanho.get(), cor.get(), valor.get(), n_id.get()))
                    conexao.commit()
                            
                    atualizada = ctk.CTkLabel(atualizacao, text='A peça foi atualizada', width=25, height=2)
                    atualizada.grid()
                            
                    def ok():
                        atualizacao.destroy()
                        tela_atualizacao.destroy()
                            
                    botao_ok = ctk.CTkButton(atualizacao, text='OK', command=ok)
                    botao_ok.grid()
                        
                else:
                        
                    def ok():
                        atualizacao.destroy()

                    botao_ok = ctk.CTkButton(atualizacao, text='OK', command=ok)
                    botao_ok.grid()

                atualizacao.mainloop()
                        
                tela_atualizacao.destroy()
                    
            botao_atualizar = ctk.CTkButton(tela_atualizacao, text='Atualizar', command=atualizar)
            botao_atualizar.grid(row=5, column=1,)
                    
            tela_atualizacao.mainloop()

        botao_atualizar_peca = ctk.CTkButton(menu_principal, text='Atualizar Uma Peça', width=25, command=atualizar_peca)
        botao_atualizar_peca.grid(row=4)
        
        menu_principal.mainloop()
    
    else:
        
        messagebox.showinfo('Senha Incorreta', 'A senha está incorreta. Digite novamente.')
        
        senha.delete(0, ctk.END)

botao_entrar = ctk.CTkButton(login, text='Entrar', command=fazer_login)
botao_entrar.grid(row=2, columnspan=2)
 
login.mainloop()