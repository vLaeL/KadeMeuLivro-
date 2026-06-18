import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from database.connection import DatabaseManager
from database.repository import FavoriteRepository

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PURPLE       = "#8345b0"
PURPLE_DARK  = "#5e2e80"
PURPLE_LIGHT = "#b07ae0"
BG           = "#1a1a2e"
SURFACE      = "#16213e"
CARD_BG      = "#0f0f23"
TEXT         = "#e0d6f5"
MUTED        = "#9e8faf"


class BookDetails:
    def __init__(self, janela_home, details_book,usuario):
        self.janela_home  = janela_home
        self.details_book = details_book
        self.usuario = usuario

        db = DatabaseManager()
        db.create_tables()
        session = db.create_session()
        self.repository = FavoriteRepository(session)

        self.janela = ctk.CTkToplevel(janela_home)
        self.janela.title(details_book.get("Título", "Detalhes do Livro"))
        self.janela.resizable(False, True)
        self.janela.configure(fg_color=BG)
        self.janela.grab_set()
        self.janela.focus()

        self._build_ui()
        self._centralizar(620, 780)

    def _centralizar(self, largura, altura):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth()  // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura  // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _build_ui(self):
        header = ctk.CTkFrame(self.janela, fg_color=SURFACE, corner_radius=0)
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text=self.details_book.get("Título", "—"),
            font=ctk.CTkFont("Georgia", 20, "bold"),
            text_color=PURPLE_LIGHT,
            wraplength=500, justify="left",
        ).pack(padx=24, pady=(20, 4), anchor="w")

        ctk.CTkLabel(
            header,
            text=self.details_book.get("Autor", "—"),
            font=ctk.CTkFont("Arial", 13),
            text_color=MUTED,
        ).pack(padx=24, pady=(0, 16), anchor="w")

        body = ctk.CTkScrollableFrame(
            self.janela, fg_color=BG,
            scrollbar_button_color=PURPLE,
        )
        body.pack(fill="both", expand=True)

        ctk.CTkLabel(
            body, text="Descrição",
            font=ctk.CTkFont("Georgia", 15, "bold"),
            text_color=PURPLE, anchor="w",
        ).pack(padx=24, pady=(20, 6), fill="x")

        desc_box = ctk.CTkTextbox(
            body, height=180, corner_radius=10,
            fg_color=SURFACE, text_color=TEXT,
            font=ctk.CTkFont("Arial", 12),
            activate_scrollbars=True,
        )
        desc_box.pack(padx=24, fill="x")
        desc_box.insert("end", self.details_book.get("Descrição", "Sem descrição disponível."))
        desc_box.configure(state="disabled")

        ctk.CTkButton(
            body, text="❤️ Adicionar aos Favoritos",
            height=42, corner_radius=10,
            fg_color=SURFACE, hover_color="#1e1e3a",
            border_width=1, border_color=PURPLE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            text_color=TEXT, command=self.add_favorite,
        ).pack(padx=24, pady=(16, 4), fill="x")

        ctk.CTkFrame(body, height=1, fg_color=PURPLE).pack(fill="x", padx=24, pady=20)

        ctk.CTkLabel(
            body, text="Informações",
            font=ctk.CTkFont("Georgia", 15, "bold"),
            text_color=PURPLE, anchor="w",
        ).pack(padx=24, pady=(0, 12), fill="x")

        info_frame = ctk.CTkFrame(body, fg_color=SURFACE, corner_radius=12)
        info_frame.pack(padx=24, fill="x")

        infos = [
            ("📄  Páginas",   self.details_book.get("Num Páginas", "—")),
            ("🏢  Editora",   self.details_book.get("Editora",     "—")),
            ("📅  Publicado", self.details_book.get("Publicado",   "—")),
            ("⭐  Nota",      self.details_book.get("Nota",        "—")),
        ]

        for i, (label, value) in enumerate(infos):
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=(12 if i == 0 else 0, 12))

            ctk.CTkLabel(
                row, text=label,
                font=ctk.CTkFont("Arial", 12), text_color=MUTED,
                width=120, anchor="w",
            ).pack(side="left")

            ctk.CTkLabel(
                row, text=str(value),
                font=ctk.CTkFont("Arial", 12, "bold"), text_color=TEXT,
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            if i < len(infos) - 1:
                ctk.CTkFrame(info_frame, height=1, fg_color=CARD_BG).pack(fill="x", padx=16)

        ctk.CTkButton(
            body, text="🛒  Comprar Agora",
            height=46, corner_radius=10,
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            font=ctk.CTkFont("Arial", 14, "bold"),
            text_color="white", command=self.link_buy,
        ).pack(padx=24, pady=24, fill="x")

    def link_buy(self):
        url = self.details_book.get("Link de Compra", "")
        if url:
            webbrowser.open(url)
        else:
            messagebox.showinfo("Indisponível", "Link de compra não disponível para este livro.")

    def add_favorite(self):
        if self.repository.is_favorite(
            self.usuario.id,
            self.details_book["ID"]
        ):
            messagebox.showinfo(
                "Favoritos",
                "Este livro já foi adicionado aos favoritos."
            )
            return

        self.repository.add_favorite(
            self.usuario.id,
            self.details_book
        )

        messagebox.showinfo(
            "Favoritos",
            "Livro adicionado aos favoritos!"
        )

        