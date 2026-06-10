import tkinter as tk
from tkinter import messagebox
from screens.home_screen import HomeWind

class LoginWind:

    def __init__(self):

        self.janela = tk.Tk()

        self.janela.title("LivrarIA Login")

        self.janela.geometry("300x200")

        self.janela.resizable(False,False)

        self.email = tk.Label(
            self.janela,
            text="Escreva seu email:"
        )
        self.email.pack()

        self.emailentry = tk.Entry(self.janela)
        self.emailentry.pack()

        self.senha = tk.Label(
            self.janela,
            text="Escreva sua senha:"
        )
        self.senha.pack()

        self.senhaentry = tk.Entry(
            self.janela,
            show="*"
        )
        self.senhaentry.pack()

        self.botao = tk.Button(
            self.janela,
            text="Enviar",
            command=self.enviar
        )
        self.botao.pack()

        self.botao_esqueceu = tk.Button(
            self.janela,
            text="Esqueceu a Senha",
            command=None
        )
        self.botao_esqueceu.pack(
            pady="10"
        )

        self.botao_registrar = tk.Button(
            self.janela,
            text="Registrar",
            command=self.abrir_registrar
        )
        self.botao_registrar.pack(
            pady="10"
        )

    def enviar(self):

        email = self.emailentry.get()

        senha = self.senhaentry.get()

        try:

            if (
                email.lower() == "1"
                and senha == "2"
            ):

                messagebox.showinfo(
                    "Sucesso",
                    "Logado com Sucesso!"
                )
                self.janela.destroy()
                self.abrir_home() 
            else:

                messagebox.showerror(
                    "Erro",
                    "Erro ao logar"
                )

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Erro de valor"
            )
    
    def abrir_home(self):
        home = HomeWind()
        home.janela.mainloop()
    
    def abrir_registrar(self):
        self.janela.destroy()
        from screens.register_screen import RegisterWind
        RegisterWind()
        