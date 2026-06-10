import tkinter as tk
from tkinter import messagebox
from screens.login_screen import LoginWind

class RegisterWind:

    def __init__(self):
        self.janela = tk.Tk()

        self.janela.title("LivrarIA Registro")

        self.janela.geometry("300x250")

        self.janela.resizable(False,False)

        self.nome = tk.Label( # Area de digitar o nome
            self.janela, 
            text="Nome completo:"
        )
        self.nome.pack()
        self.nomeentry = tk.Entry(self.janela)
        self.nomeentry.pack()
        
        self.email = tk.Label( # Area de digitar o email
            self.janela,
            text="Email:"
        )
        self.email.pack()
        self.emailentry = tk.Entry(self.janela)
        self.emailentry.pack()

        self.senhaprimlab = tk.Label( #digitar a senha
            self.janela,
            text="Digite uma senha:"
        )
        self.senhaprimlab.pack()
        self.senhaprimentry = tk.Entry(self.janela)
        self.senhaprimentry.pack()

        self.senhaseclab = tk.Label( #digitar novamente a senha
            self.janela,
            text="Digite novamente:"
        )
        self.senhaseclab.pack()
        self.senhaseconentry = tk.Entry(self.janela)
        self.senhaseconentry.pack()

        self.botao = tk.Button(
            self.janela,
            text="Registrar",
            command=self.enviar,
            width="10"
        )
        self.botao.pack(
            pady="15"
        )
    
    def org_nome(self,nome):
        nome = self.nomeentry.get()
        nome.capitalize()
        return True
    
    def validar_email(self,email):
        email = self.emailentry.get()
        if "@" not in email or "." not in email:
            messagebox.showerror("Erro", "Email Inválido")
            return False  
        return True    

    def validar_senha(self,senha):
        senha = self.senhaprimentry.get()
        c_diferente = "!@#()?/"

        if not any(caracter in c_diferente for caracter in senha):
            messagebox.showerror("Erro","Senha sem Caracter Especial !@#()?/ ")
            return False
        
            
        if not any(caracter.isdigit() for caracter in senha):
            messagebox.showerror("Erro","A senha precisa de pelo menos 1 digito! ")
            return False
        
        if len(senha) < 8:
            messagebox.showerror("Error","Sua senha deve contér 8 caracteres!")
            return False
        
        return True
        
        
    def confirm_senha(self,senha1,senha2):
        senha1 = self.senhaprimentry.get()
        senha2 = self.senhaseconentry.get()        
        if senha1 != senha2:
            messagebox.showerror("Erro","As senhas não coincidem!")
            return False
        return True

    def enviar(self):
        nome = self.nomeentry.get()
        email = self.emailentry.get()
        senha1 = self.senhaprimentry.get()
        senha2 = self.senhaseconentry.get()
        nome_mensg = nome.split()
        try:

           if ( 
            self.validar_email(email) and
            self.validar_senha(senha1) and
            self.confirm_senha(senha1,senha2) and
            self.org_nome(nome) == True 
            ):
            messagebox.showinfo(
                "Regitro",
                f"{nome_mensg[0]}, você foi registrado com sucesso!"
            )
            self.janela.destroy()
            self.abrir_login() 
        except:
            messagebox.showerror(
                "Error",
                "Erro inesperado"
            )
            return False
        
    def abrir_login(self):
        LoginWind()



#teste1 = RegisterWind()
#teste1.janela.mainloop()