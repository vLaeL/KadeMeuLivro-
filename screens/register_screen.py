import customtkinter as ctk
from tkinter import messagebox
from database import connection,repository

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PURPLE      = "#8345b0"
PURPLE_DARK = "#5e2e80"
BG          = "#1a1a2e"
SURFACE     = "#16213e"
TEXT        = "#e0d6f5"
MUTED       = "#9e8faf"
ERROR       = "#e05c5c"


class RegisterWind:
    def __init__(self, janela_pai = None):

        db = connection.DatabaseManager()
        db.create_tables()
        session = db.create_session()
        self.repository = repository.UserRepository(session)

        if janela_pai is None:
            self.janela = ctk.CTk()
        else:
            self.janela = ctk.CTkToplevel(janela_pai)    
        self.janela.title("kadeMeuLivro — Registro")
        self.janela.resizable(False, False)
        self.janela.configure(fg_color=BG)

        self._build_ui()
        self._centralizar(440, 620)
        self.janela.mainloop()

    def _centralizar(self, largura, altura):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth()  // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura  // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _build_ui(self):
        ctk.CTkLabel(
            self.janela, text="📚  kadeMeuLivro",
            font=ctk.CTkFont("Georgia", 28, "bold"), text_color=PURPLE,
        ).pack(pady=(40, 2))
        ctk.CTkLabel(
            self.janela, text="Crie sua conta",
            font=ctk.CTkFont("Arial", 13), text_color=MUTED,
        ).pack(pady=(0, 24))

        card = ctk.CTkFrame(self.janela, fg_color=SURFACE, corner_radius=16)
        card.pack(padx=40, fill="x")

        def field(parent, label, placeholder, show=None):
            ctk.CTkLabel(parent, text=label, font=ctk.CTkFont("Arial", 12),
                         text_color=MUTED, anchor="w").pack(padx=24, pady=(16, 2), fill="x")
            entry = ctk.CTkEntry(
                parent, placeholder_text=placeholder,
                height=40, corner_radius=8, show=show or "",
                fg_color="#0f0f23", border_color=PURPLE,
                text_color=TEXT, font=ctk.CTkFont("Arial", 13),
            )
            entry.pack(padx=24, fill="x")
            return entry

        self.nomeentry       = field(card, "Nome completo",    "João Silva")
        self.emailentry      = field(card, "E-mail",           "seu@email.com")
        self.senhaprimentry  = field(card, "Senha",            "Min. 8 caracteres", show="•")
        self.senhaseconentry = field(card, "Confirmar senha",  "Repita a senha",    show="•")

        ctk.CTkButton(
            card, text="Criar conta",
            height=44, corner_radius=10,
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            font=ctk.CTkFont("Arial", 14, "bold"),
            text_color="white", command=self.enviar,
        ).pack(padx=24, pady=(20, 24), fill="x")

        footer = ctk.CTkFrame(self.janela, fg_color="transparent")
        footer.pack(pady=16)
        ctk.CTkLabel(footer, text="Já tem conta?",
                     text_color=MUTED, font=ctk.CTkFont("Arial", 12)).pack(side="left")
        ctk.CTkButton(
            footer, text=" Entrar",
            fg_color="transparent", hover=False,
            text_color=PURPLE, font=ctk.CTkFont("Arial", 12, "bold"),
            command=self.abrir_login,
        ).pack(side="left")

    # ── validações ────────────────────────────────────────────────────────────

    def org_nome(self, nome):
        return bool(nome.strip())

    def validar_email(self, email):
        if "@" not in email or "." not in email:
            messagebox.showerror("Erro", "E-mail inválido.")
            return False
        return True

    def validar_senha(self, senha):
        especiais = "!@#()?/"
        if not any(c in especiais for c in senha):
            messagebox.showerror("Erro", "A senha precisa de um caractere especial: !@#()?/")
            return False
        if not any(c.isdigit() for c in senha):
            messagebox.showerror("Erro", "A senha precisa de ao menos 1 dígito.")
            return False
        if len(senha) < 8:
            messagebox.showerror("Erro", "A senha deve ter ao menos 8 caracteres.")
            return False
        return True

    def confirm_senha(self, s1, s2):
        if s1 != s2:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return False
        return True

    def enviar(self):
        nome   = self.nomeentry.get().strip()
        email  = self.emailentry.get().strip()
        senha1 = self.senhaprimentry.get()
        senha2 = self.senhaseconentry.get()
        nome_split = nome.split()
        

    def enviar(self):
        nome = self.nomeentry.get().strip()
        email = self.emailentry.get().strip()
        senha1 = self.senhaprimentry.get()
        senha2 = self.senhaseconentry.get()
        nome_split = nome.split()

        if not self.org_nome(nome):
            return

        if not self.validar_email(email):
            return

        if not self.validar_senha(senha1):
            return

        if not self.confirm_senha(senha1, senha2):
            return

        try:
            self.repository.create_user(nome, email, senha1)
        except Exception as e:
            print(e)
            messagebox.showerror("Erro", f"Erro ao registrar:\n{e}")
            return

        messagebox.showinfo(
            "Registro",
            f"{nome_split[0]}, você fez seu registro com sucesso!"
        )

        self.janela.destroy()
        self.abrir_login()

    def abrir_login(self):
        from screens.login_screen import LoginWind
        LoginWind()
        



if __name__ == "__main__":
    RegisterWind()