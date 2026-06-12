import customtkinter as ctk
from tkinter import messagebox
from services.google_books_service import GoogleBookApi
from screens.login_screen import LoginWind
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PURPLE      = "#8345b0"
PURPLE_DARK = "#5e2e80"
PURPLE_LIGHT= "#b07ae0"
BG          = "#1a1a2e"
SURFACE     = "#16213e"
CARD_BG     = "#0f0f23"
TEXT        = "#e0d6f5"
MUTED       = "#9e8faf"
DIVIDER     = "#2a2a4a"
RED         = "#e05c5c"


class ProfileWind:
    def __init__(self, janela_pai=None, usuario = None):
        self.usuario = usuario
        self.janela_pai = janela_pai
        self._open_windows = {}

        if janela_pai is not None:
            self.janela = ctk.CTkToplevel(janela_pai)
        else:
            self.janela = ctk.CTk()

        self.janela.title("kadeMeuLivro — Perfil")
        self.janela.resizable(False, False)
        self.janela.configure(fg_color=BG)

        self._build_ui()
        self._centralizar(860, 480)

        if janela_pai is None:
            self.janela.mainloop()

    def _centralizar(self, largura, altura):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth()  // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura  // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _build_ui(self):
        letra_usuario = self.usuario.nome[0]
        usuario_nome = self.usuario.nome.split()
        usuario_email = self.usuario.email
        outer = ctk.CTkFrame(self.janela, fg_color=BG)
        outer.pack(fill="both", expand=True, padx=20, pady=20)

        # ── Coluna esquerda ───────────────────────────────────────────────────
        left = ctk.CTkFrame(outer, fg_color=SURFACE, corner_radius=16, width=220)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)

        # Avatar circular com iniciais
        avatar = ctk.CTkFrame(left, fg_color=PURPLE, width=90, height=90, corner_radius=45)
        avatar.pack(pady=(32, 12))
        avatar.pack_propagate(False)
        ctk.CTkLabel(
            avatar, text=letra_usuario,
            font=ctk.CTkFont("Arial", 28, "bold"), text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            left, text=f"{usuario_nome[0]} {usuario_nome[-1]}",
            font=ctk.CTkFont("Arial", 14, "bold"), text_color=TEXT,
        ).pack()

        ctk.CTkLabel(
            left, text=usuario_email,
            font=ctk.CTkFont("Arial", 11), text_color=MUTED,
        ).pack(pady=(2, 20))

        ctk.CTkButton(
            left, text="✏️  Editar perfil",
            height=36, corner_radius=8,
            fg_color="transparent", hover_color=CARD_BG,
            border_width=1, border_color=PURPLE,
            font=ctk.CTkFont("Arial", 12), text_color=TEXT,
            command=lambda: messagebox.showinfo("Perfil", "Funcionalidade em breve!"),
        ).pack(padx=20, fill="x")

        # Divisor
        ctk.CTkFrame(left, height=1, fg_color=DIVIDER).pack(fill="x", padx=20, pady=24)

        ctk.CTkButton(
            left, text="↩️  Sair da conta",
            height=36, corner_radius=8,
            fg_color="transparent", hover=False,
            font=ctk.CTkFont("Arial", 12, "bold"), text_color=RED,
            command=self._sair,
        ).pack(padx=20, fill="x")

        # ── Coluna direita ────────────────────────────────────────────────────
        right = ctk.CTkFrame(outer, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        # Estatísticas
        ctk.CTkLabel(
            right, text="Minhas estatísticas",
            font=ctk.CTkFont("Arial", 15, "bold"), text_color=TEXT, anchor="w",
        ).pack(fill="x", pady=(4, 12))

        stats_row = ctk.CTkFrame(right, fg_color="transparent")
        stats_row.pack(fill="x")

        stats = [
            ("📖", "12", "Livros salvos"),
            ("🕐", "28", "Buscas realizadas"),
            ("🤍", "5",  "Favoritos"),
        ]

        for emoji, valor, label in stats:
            card = ctk.CTkFrame(stats_row, fg_color=SURFACE, corner_radius=12)
            card.pack(side="left", expand=True, fill="x", padx=(0, 10))

            ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont("Arial", 22)).pack(pady=(16, 2))
            ctk.CTkLabel(
                card, text=valor,
                font=ctk.CTkFont("Arial", 22, "bold"), text_color=TEXT,
            ).pack()
            ctk.CTkLabel(
                card, text=label,
                font=ctk.CTkFont("Arial", 11), text_color=MUTED,
            ).pack(pady=(0, 16))

        # Últimas buscas
        hist_header = ctk.CTkFrame(right, fg_color="transparent")
        hist_header.pack(fill="x", pady=(24, 10))

        ctk.CTkLabel(
            hist_header, text="Últimas buscas",
            font=ctk.CTkFont("Arial", 15, "bold"), text_color=TEXT,
        ).pack(side="left")

        ctk.CTkButton(
            hist_header, text="Ver histórico completo",
            height=30, corner_radius=8,
            fg_color="transparent", hover_color=SURFACE,
            border_width=1, border_color=MUTED,
            font=ctk.CTkFont("Arial", 11), text_color=TEXT,
            command=lambda: messagebox.showinfo("Histórico", "Funcionalidade em breve!"),
        ).pack(side="right")

        buscas = [
            ("Clean Code",          "Hoje, 14:32"),
            ("Arquitetura Limpa",   "Hoje, 13:15"),
            ("Padrões de Projeto",  "Ontem, 18:45"),
        ]

        hist_frame = ctk.CTkFrame(right, fg_color=SURFACE, corner_radius=12)
        hist_frame.pack(fill="x")

        for i, (titulo, horario) in enumerate(buscas):
            row = ctk.CTkFrame(hist_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=(12 if i == 0 else 0, 12))

            ctk.CTkLabel(
                row, text=f"🕐  {titulo}",
                font=ctk.CTkFont("Arial", 12), text_color=TEXT, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=horario,
                font=ctk.CTkFont("Arial", 11), text_color=MUTED, anchor="e",
            ).pack(side="right")

            if i < len(buscas) - 1:
                ctk.CTkFrame(hist_frame, height=1, fg_color=DIVIDER).pack(fill="x", padx=16)

    # ── Controle de janela única ──────────────────────────────────────────────

    def _janela_ja_aberta(self, chave):
        instancia = self._open_windows.get(chave)
        if instancia is not None:
            try:
                if instancia.janela.winfo_exists():
                    instancia.janela.deiconify()
                    instancia.janela.lift()
                    instancia.janela.focus_force()
                    return True
            except Exception:
                pass
            del self._open_windows[chave]
        return False

    # ── Navegação ─────────────────────────────────────────────────────────────

    def _sair(self):
        self.janela.destroy()

        if self.janela_pai is not None:
            self.janela_pai.destroy()
        
        from screens.login_screen import LoginWind
        LoginWind()


if __name__ == "__main__":
    ProfileWind()