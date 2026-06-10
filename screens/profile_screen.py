import tkinter as tk
from tkinter import messagebox

class ProfileWind:
    def __init__(self,janela_home):
        self.janela_home = janela_home

        self.janela = tk.Toplevel()

        self.janela.title("LivrarIA Profile")

        self.janela.geometry("200x300")

        self.janela.resizable(False,False)


        self.nome_usuario = tk.Label(
            self.janela,
            text="Nome Completo",
            font=("Arial",15)
        )
        self.nome_usuario.pack(
            pady=("50","10")
        )

        self.email_usuario = tk.Label(
            self.janela,
            text="Usuario@gmail.com"
        )
        self.email_usuario.pack(
            pady="10"
        )

        self.editar_button = tk.Button(
            self.janela,
            text="Editar Perfil",
            command=None
        )
        self.editar_button.pack(
            pady=("10","10")
        )

        self.botao_sair =tk.Button(
            self.janela,
            text="Sair da Conta",
            command=self.sair_conta
        )
        self.botao_sair.pack(
            pady=("50","0")
        )
    
    def sair_conta(self):
        self.janela.destroy()
        self.janela_home.destroy()

        from screens.login_screen import LoginWind
        LoginWind()


