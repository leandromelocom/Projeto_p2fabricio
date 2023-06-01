import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class TelaLogin:
    def __init__(self):
        self.janela = tk.Tk()
        self.tela()
        self.widgets()
       
    def tela(self):
        self.janela.title("Login")
        self.janela.geometry('400x300')

    def widgets(self):
        self.label_username = tk.Label(self.janela, text='Login:')
        self.label_username.pack()
        self.entry_username = ttk.Entry(self.janela)
        self.entry_username.pack()

        self.label_password = tk.Label(self.janela, text="Senha:")
        self.label_password.pack()
        self.entry_password = ttk.Entry(self.janela, show="*")
        self.entry_password.pack()

        self.botao_login = tk.Button(self.janela, text="Login", command=self.fazer_login)
        self.botao_login.pack()

        self.botao_cadastrar = tk.Button(self.janela, text="Cadastrar", command=self.abrir_tela_cadastro_usuario)
        self.botao_cadastrar.pack()

        self.botao_sair = tk.Button(self.janela, text="Sair", command=self.sair)
        self.botao_sair.pack()

    def fazer_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('loja_login_adm.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result is not None:
            db_username, db_password = result

            if password == db_password:
                messagebox.showinfo("Login", "Bem-vindo, {}".format(username))
                self.abrir_tela_material()
            else:
                messagebox.showerror("Credenciais inválidas!", "Senha incorreta")
        else:
            messagebox.showerror("Credenciais inválidas!", "Usuário não cadastrado no sistema")

        conn.close()

    def sair(self):
        self.janela.destroy()

    def abrir_tela_cadastro_usuario(self):
        self.janela.withdraw()

        tela_cadastro_usuario = TelaCadastroUsuario(self)
        tela_cadastro_usuario.iniciar()

    def abrir_tela_material(self):
        self.janela.withdraw()

        tela_material = TelaMaterial(self)
        tela_material.iniciar()

    def iniciar(self):
        self.janela.mainloop()


class TelaCadastroUsuario:
    def __init__(self, tela_login):
        self.tela_login = tela_login
        self.janela_cadastro_usuario = tk.Toplevel(self.tela_login.janela)
        self.janela_cadastro_usuario.title("Cadastro de Usuário")
        self.janela_cadastro_usuario.geometry('400x300')
        self.widgets()

    def widgets(self):
        self.label_nome = tk.Label(self.janela_cadastro_usuario, text='Nome:')
        self.label_nome.pack()
        self.entry_nome = ttk.Entry(self.janela_cadastro_usuario)
        self.entry_nome.pack()

        self.label_username = tk.Label(self.janela_cadastro_usuario, text='Login:')
        self.label_username.pack()
        self.entry_username = ttk.Entry(self.janela_cadastro_usuario)
        self.entry_username.pack()

        self.label_password = tk.Label(self.janela_cadastro_usuario, text="Senha:")
        self.label_password.pack()
        self.entry_password = ttk.Entry(self.janela_cadastro_usuario, show="*")
        self.entry_password.pack()

        self.botao_registrar = tk.Button(self.janela_cadastro_usuario, text="Registrar", command=self.registrar_usuario)
        self.botao_registrar.pack()

        self.botao_fechar = tk.Button(self.janela_cadastro_usuario, text="Fechar", command=self.fechar_janela)
        self.botao_fechar.pack()

    def registrar_usuario(self):
        nome = self.entry_nome.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sqlite3.connect('loja_login_adm.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result is not None:
            messagebox.showerror("Usuário já existe", "O usuário já está cadastrado no sistema")
        else:
            cursor.execute("INSERT INTO usuarios (nome, username, password) VALUES (?, ?, ?)",
                           (nome, username, password))
            conn.commit()

            messagebox.showinfo("Registro", "Usuário registrado com sucesso")
            self.fechar_janela()
            self.tela_login.abrir_tela_material()

        conn.close()

    def fechar_janela(self):
        self.janela_cadastro_usuario.destroy()
        self.tela_login.janela.deiconify()

    def iniciar(self):
        self.janela_cadastro_usuario.mainloop()


class TelaMaterial:
    def __init__(self, tela_login):
        self.tela_login = tela_login
        self.janela_material = tk.Toplevel(self.tela_login.janela)
        self.janela_material.title("Cadastro de Material")
        self.janela_material.geometry('400x300')
        self.widgets()

    def widgets(self):
        self.label_nome_material = tk.Label(self.janela_material, text='Nome do material:')
        self.label_nome_material.pack()
        self.entry_nome_material = ttk.Entry(self.janela_material)
        self.entry_nome_material.pack()

        self.label_quantidade = tk.Label(self.janela_material, text="Quantidade:")
        self.label_quantidade.pack()
        self.entry_quantidade = ttk.Entry(self.janela_material)
        self.entry_quantidade.pack()

        self.botao_registrar = tk.Button(self.janela_material, text="Registrar", command=self.registrar_material)
        self.botao_registrar.pack()

        self.botao_excluir = tk.Button(self.janela_material, text="Excluir", command=self.excluir_material)
        self.botao_excluir.pack()

        self.botao_modificar = tk.Button(self.janela_material, text="Modificar", command=self.modificar_material)
        self.botao_modificar.pack()

        self.botao_fechar = tk.Button(self.janela_material, text="Fechar", command=self.fechar_janela)
        self.botao_fechar.pack()

    def registrar_material(self):
        nome_material = self.entry_nome_material.get()
        quantidade = self.entry_quantidade.get()

        conn = sqlite3.connect('loja_estoque.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM materiais WHERE nome = ?", (nome_material,))
        result = cursor.fetchone()

        if result is not None:
            messagebox.showerror("Cadastro do Material", "Material {} já cadastrado".format(nome_material))
        else:
            cursor.execute("INSERT INTO materiais (nome, quantidade) VALUES (?, ?)",
                           (nome_material, quantidade))
            conn.commit()

            messagebox.showinfo("Registro", "Material registrado com sucesso")

        conn.close()

    def excluir_material(self):
        nome_material = self.entry_nome_material.get()

        conn = sqlite3.connect('loja_estoque.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM materiais WHERE nome = ?", (nome_material,))
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror("Excluir Material", "Material {} não encontrado".format(nome_material))
        else:
            cursor.execute("DELETE FROM materiais WHERE nome = ?", (nome_material,))
            conn.commit()

            messagebox.showinfo("Excluir Material", "Material excluído com sucesso")

        conn.close()

    def modificar_material(self):
        nome_material = self.entry_nome_material.get()
        quantidade = self.entry_quantidade.get()

        conn = sqlite3.connect('loja_estoque.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM materiais WHERE nome = ?", (nome_material,))
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror("Modificar Material", "Material {} não encontrado".format(nome_material))
        else:
            cursor.execute("UPDATE materiais SET quantidade = ? WHERE nome = ?", (quantidade, nome_material))
            conn.commit()

            messagebox.showinfo("Modificar Material", "Material modificado com sucesso")

        conn.close()

    def fechar_janela(self):
        self.janela_material.destroy()
        self.tela_login.janela.deiconify()

    def iniciar(self):
        self.janela_material.mainloop()


if __name__ == "__main__":

    conn = sqlite3.connect('loja_login_adm.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (nome TEXT, username TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

    conn = sqlite3.connect('loja_estoque.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS materiais (nome TEXT PRIMARY KEY, quantidade TEXT)")
    conn.commit()
    conn.close()

    tela = TelaLogin()
    tela.iniciar()




