import customtkinter as ctk
from tkinter import messagebox
from database.connection import DatabaseManager
from database.repository import FavoriteRepository

PURPLE = "#6F18AD"
PURPLE_DARK = "#460574"
BG = "#000214"
SURFACE = "#111B33"
CARD_BG = "#05081A"
TEXT = "#E0D6F5"
MUTED = "#9E8FAF"
RED = "#e05c5c"


class FavoritesWind:
    def __init__(self, janela_pai=None, usuario=None):
        self.janela_pai = janela_pai
        self.usuario = usuario
        if janela_pai is not None:
            self.janela = ctk.CTkToplevel(janela_pai)
        else:
            self.janela = ctk.CTk()
        db = DatabaseManager()
        db.create_tables()
        session = db.create_session()
        self.repository = FavoriteRepository(session)

        self.janela.title("kadeMeuLivro — Favoritos")
        self.janela.geometry("800x600")
        self.janela.resizable(False, False)
        self.janela.configure(fg_color=BG)

        self._build_ui()
        self.carregar_favoritos()

        if janela_pai is None:
            self.janela.mainloop()

    def _build_ui(self):
        ctk.CTkLabel(
            self.janela,
            text="❤️ Favoritos",
            font=ctk.CTkFont("Georgia", 26, "bold"),
            text_color=PURPLE
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self.janela,
            text="Livros que você salvou para ver depois",
            font=ctk.CTkFont("Arial", 13),
            text_color=MUTED
        ).pack(pady=(0, 20))

        self.favorites_frame = ctk.CTkScrollableFrame(
            self.janela,
            fg_color=CARD_BG,
            corner_radius=12,
            scrollbar_button_color=PURPLE
        )
        self.favorites_frame.pack(fill="both", expand=True, padx=32, pady=(0, 24))

        self.show_favorites([])
    
    def carregar_favoritos(self):
        favoritos = self.repository.get_user_fav(self.usuario.id)

        favoritos_dict = [
            favorito.to_dict()
            for favorito in favoritos
        ]

        self.show_favorites(favoritos_dict)

    def show_favorites(self, favoritos):
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()

        if not favoritos:
            ctk.CTkLabel(
                self.favorites_frame,
                text="Nenhum livro favorito ainda.",
                font=ctk.CTkFont("Arial", 15),
                text_color=MUTED
            ).pack(pady=80)
            return

        for livro in favoritos:
            self._favorite_card(livro)

    def _favorite_card(self, livro):
        card = ctk.CTkFrame(
            self.favorites_frame,
            fg_color=SURFACE,
            corner_radius=12
        )
        card.pack(fill="x", padx=10, pady=8)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        ctk.CTkLabel(
            info,
            text=livro.get("title", "Sem título"),
            font=ctk.CTkFont("Georgia", 15, "bold"),
            text_color=TEXT,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info,
            text=livro.get("autor", "Autor desconhecido"),
            font=ctk.CTkFont("Arial", 12),
            text_color=MUTED,
            anchor="w"
        ).pack(fill="x", pady=(4, 0))

        ctk.CTkButton(
            card,
            text="Remover",
            width=110,
            height=34,
            corner_radius=8,
            fg_color=RED,
            hover_color="#b93f3f",
            font=ctk.CTkFont("Arial", 12, "bold"),
            command=lambda: self.remover_favorito(livro)
        ).pack(side="right", padx=16, pady=14)

        ctk.CTkButton(
            card,
            text="Visualizar",
            width=110,
            height=34,
            corner_radius=8,
            fg_color=PURPLE,
            hover_color="#6a2abd",
            font=ctk.CTkFont("Arial", 12, "bold"),
            command=lambda: self.abrir_descricao(livro)
        ).pack(side="right", padx=8, pady=14)


    def remover_favorito(self, livro):
        sucesso = self.repository.delete_favorite(
        self.usuario.id,
        livro["book_id"]
        )
        if sucesso:
            messagebox.showinfo(
                "Favoritos",
                f"Você removeu este livro dos favoritos."
            )
            self.carregar_favoritos()
        else:
            messagebox.showerror(
                "Favoritos Error",
                f"Erro ao remover este livro dos favoritos."
            )
            
    def abrir_descricao(self, livro):
        detalhes = {
            "ID": livro.get("book_id"),
            "Título": livro.get("title", "Sem título"),
            "Autor": livro.get("autor", "Autor desconhecido"),
            "Descrição": livro.get("descricao", "Sem descrição disponível."),
            "Idioma": livro.get("idioma", "Indisponível"),
            "Preço": livro.get("preco", "Indisponível"),
            "Link de Compra": livro.get("link_compra", ""),
            "Imagem": livro.get("imagem", "Sem imagem"),
            "Editora": livro.get("editora", "Editora não informada"),
            "Publicado": livro.get("publicado", "Data indisponível"),
            "Num Páginas": livro.get("num_paginas", "Quantidade indisponível"),
            "Nota": livro.get("nota", "Sem avaliação")
        }

        from screens.book_details_screen import BookDetails
        BookDetails(self.janela, detalhes, self.usuario)

if __name__ == "__main__":
    FavoritesWind()