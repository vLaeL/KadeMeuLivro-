import customtkinter as ctk
from tkinter import messagebox
from database import connection, repository

PURPLE = "#6F18AD"
PURPLE_DARK = "#460574"
BG = "#000214"
SURFACE = "#111B33"
TEXT = "#E0D6F5"
MUTED = "#9E8FAF"


class ForgotWind:
    def __init__(self, janela_pai=None):
        db = connection.DatabaseManager()
        db.create_tables()
        session = db.create_session()
        self.repository = repository.UserRepository(session)

        self.janela_pai = janela_pai

        if janela_pai is not None:
            self.janela = ctk.CTkToplevel(janela_pai)
        else:
            self.janela = ctk.CTk()

        self.janela.title("KadeMeuLivro — Esqueci a Senha")
        self.janela.geometry("420x360")
        self.janela.resizable(False, False)
        self.janela.configure(fg_color=BG)

        self._build_ui()
        self._centralizar(420, 460)

        if janela_pai is None:
            self.janela.mainloop()

    def _centralizar(self, largura, altura):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _build_ui(self):
        ctk.CTkLabel(
            self.janela,
            text="🔐 Recuperar senha",
            font=ctk.CTkFont("Georgia", 24, "bold"),
            text_color=PURPLE
        ).pack(pady=(32, 6))

        ctk.CTkLabel(
            self.janela,
            text="Digite seu e-mail e escolha uma nova senha.",
            font=ctk.CTkFont("Arial", 12),
            text_color=MUTED
        ).pack(pady=(0, 20))

        card = ctk.CTkFrame(self.janela, fg_color=SURFACE, corner_radius=16)
        card.pack(padx=36, fill="x")

        self.email_entry = self._field(card, "E-mail", "seu@email.com")
        self.nova_senha_entry = self._field(card, "Nova senha", "Nova senha", show="•")
        self.confirmar_senha_entry = self._field(card, "Confirmar senha", "Repita a nova senha", show="•")

        ctk.CTkButton(
            card,
            text="Alterar senha",
            height=42,
            corner_radius=10,
            fg_color=PURPLE,
            hover_color=PURPLE_DARK,
            font=ctk.CTkFont("Arial", 13, "bold"),
            text_color="white",
            command=self.alterar_senha
        ).pack(padx=24, pady=(20, 24), fill="x")

    def _field(self, parent, label, placeholder, show=None):
        ctk.CTkLabel(
            parent,
            text=label,
            font=ctk.CTkFont("Arial", 12),
            text_color=MUTED,
            anchor="w"
        ).pack(padx=24, pady=(14, 2), fill="x")

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=38,
            corner_radius=8,
            show=show or "",
            fg_color="#0f0f23",
            border_color=PURPLE,
            text_color=TEXT,
            font=ctk.CTkFont("Arial", 12)
        )
        entry.pack(padx=24, fill="x")
        return entry

    def alterar_senha(self):
        email = self.email_entry.get().strip()
        nova_senha = self.nova_senha_entry.get()
        confirmar_senha = self.confirmar_senha_entry.get()

        usuario = self.repository.get_by_email(email)

        if usuario is None:
            messagebox.showerror("Erro", "E-mail não encontrado.")
            return

        if nova_senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return

        if len(nova_senha) < 8:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 8 caracteres.")
            return

        resultado = self.repository.update_password(usuario.id, nova_senha)

        if resultado:
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")
            self.janela.destroy()
        else:
            messagebox.showerror("Erro", "Não foi possível alterar a senha.")


if __name__ == "__main__":
    ForgotWind()