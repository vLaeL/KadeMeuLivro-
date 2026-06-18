import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw
import os
import cv2
import threading
import time
from services.google_books_service import GoogleBookApi

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PURPLE      = "#6F18AD"
PURPLE_DARK = "#460574"
PURPLE_LIGHT= "#A25CFF"
BG          = "#000214"
BG_ALT      = "#05081A"
SURFACE     = "#111B33"
CARD_BG     = "#05081A"
TEXT        = "#E0D6F5"
MUTED       = "#9E8FAF"
ACCENT      = "#8B3DFF"
ACCENT_HOVER= "#A25CFF"
DIVIDER     = "#1a1a3a"
DROPDOWN_BG = "#111B33"


class HomeWind:
    def __init__(self, usuario):
        self.usuario = usuario
        self.janela = ctk.CTk()
        self.janela.title("kadeMeuLivro — Home")
        self.janela.resizable(True, True)
        self.janela.configure(fg_color=BG)
        self.janela.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.livros_resultados = []
        self._open_windows  = {}
        self._dropdown_win  = None
        self.video_running  = True
        self.video_label    = None
        self.video_capture  = None

        self._build_ui()
        self._centralizar(1100, 700)
        self.janela.mainloop()

    def _centralizar(self, largura, altura):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth()  // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura  // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _on_closing(self):
        """Para o vídeo e fecha a aplicação corretamente"""
        self.video_running = False
        time.sleep(0.05)
        if self.video_capture:
            self.video_capture.release()
        self.janela.destroy()

    def _play_video(self):
        """Toca o vídeo em loop, agendando updates na thread principal"""
        while self.video_running:
            try:
                ret, frame = self.video_capture.read()
                if not ret:
                    self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                frame = cv2.resize(frame, (300, 140))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)
                ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(300, 140))
                if self.video_running:
                    self.janela.after(0, self._atualizar_frame, ctk_image)
                time.sleep(0.033)
            except Exception:
                break

    def _atualizar_frame(self, ctk_image):
        """Chamado pela thread principal via after() — seguro contra race conditions"""
        try:
            if self.video_running and self.janela.winfo_exists() and self.video_label:
                self.video_label.configure(image=ctk_image)
        except Exception:
            pass

    def _lupa_icon(self):
        """Gera ícone de lupa como CTkImage (branco, 24x24)"""
        size = 24
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Círculo da lupa
        draw.ellipse([2, 2, 16, 16], outline="white", width=2)
        # Cabo da lupa
        draw.line([13, 13, 21, 21], fill="white", width=2)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    def _build_ui(self):
        # ── Top bar (sem frame, igual ao login) ─────────────────────────────
        topbar = ctk.CTkFrame(self.janela, fg_color="transparent", height=155, corner_radius=0)
        topbar.pack(fill="x", padx=24, pady=(0, 0))
        topbar.pack_propagate(False)

        # Vídeo do logo à esquerda — igual ao login
        video_path = os.path.join(os.path.dirname(__file__), "..", "assets", "imagens", "pixel cat.mp4")
        self.video_label = ctk.CTkLabel(topbar, text="", fg_color="transparent")
        self.video_label.pack(side="left", anchor="n", pady=(0, 0))
        self.video_capture = cv2.VideoCapture(video_path)
        video_thread = threading.Thread(target=self._play_video, daemon=True)
        video_thread.start()

        self.btn_perfil = ctk.CTkButton(
            topbar, text="👤  Perfil  ▾",
            width=130, height=36, corner_radius=8,
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            font=ctk.CTkFont("Arial", 12, "bold"),
            command=self._toggle_dropdown,
        )
        self.btn_perfil.pack(side="right", anchor="n", pady=(12, 0))

        # ── Barra de busca ───────────────────────────────────────────────────
        search_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        search_frame.pack(fill="x", padx=40, pady=28)

        ctk.CTkLabel(
            search_frame, text="Buscar Livros",
            font=ctk.CTkFont("Georgia", 20, "bold"), text_color=TEXT,
        ).pack(anchor="center", pady=(0, 10))

        # Container pill — imita o .searchBox do Uiverse
        # height = 54 (entry) + 4 padding top + 4 padding bottom = 62
        PILL_H = 62
        PILL_W = 480  # largura total da pill

        pill = ctk.CTkFrame(
            search_frame,
            fg_color=SURFACE,
            corner_radius=PILL_H // 2,
            border_width=1,
            border_color=PURPLE,
            width=PILL_W,
            height=PILL_H,
        )
        pill.pack(anchor="center")
        pill.pack_propagate(False)  # mantém tamanho fixo

        # Entry ocupa a pill toda menos o espaço do botão à direita
        self.buscarEntry = ctk.CTkEntry(
            pill,
            placeholder_text="Título, autor ou ISBN…",
            width=PILL_W - 70,  # deixa 70px para o botão + margem
            height=PILL_H - 8,
            corner_radius=PILL_H // 2,
            fg_color="transparent",
            border_width=0,
            text_color=TEXT,
            placeholder_text_color=MUTED,
            font=ctk.CTkFont("Arial", 14),
        )
        self.buscarEntry.place(x=20, rely=0.5, anchor="w")
        self.buscarEntry.bind("<Return>", lambda e: self.consult_push())

        
        self.buscarbotao = ctk.CTkButton(
            pill,
            text="",
            image=self._lupa_icon(),
            width=50, height=50,
            corner_radius=25,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            command=self.consult_push,
        )
        self.buscarbotao.place(relx=1.0, rely=0.5, anchor="e", x=-6)

        # ── Área de resultados ───────────────────────────────────────────────
        self.results_frame = ctk.CTkScrollableFrame(
            self.janela, fg_color=CARD_BG,
            corner_radius=12, scrollbar_button_color=ACCENT,
        )
        self.results_frame.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        self._empty_state()

    def _empty_state(self):
        for w in self.results_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(
            self.results_frame,
            text="🔍  Pesquise um livro para começar",
            font=ctk.CTkFont("Arial", 15), text_color=MUTED,
        ).pack(expand=True, pady=60)

    # ── Dropdown de perfil ────────────────────────────────────────────────────

    def _toggle_dropdown(self):
        if self._dropdown_win is not None:
            try:
                if self._dropdown_win.winfo_exists():
                    self._fechar_dropdown()
                    return
            except Exception:
                pass
            self._dropdown_win = None
        self._abrir_dropdown()

    def _abrir_dropdown(self):
        self.btn_perfil.configure(text="👤  Perfil  ▴")

        self.janela.update_idletasks()
        bx = self.btn_perfil.winfo_rootx()
        by = self.btn_perfil.winfo_rooty() + self.btn_perfil.winfo_height() + 4

        popup = ctk.CTkToplevel(self.janela)
        popup.overrideredirect(True)
        popup.configure(fg_color=DROPDOWN_BG)
        popup.geometry(f"210x150+{bx - 76}+{by}")
        popup.lift()
        self._dropdown_win = popup

        self.janela.bind("<Button-1>", self._fechar_se_fora, add="+")

        itens = [
            ("👤  Visualizar Perfil", self._ir_perfil),
            ("❤️  Favoritos",          self._ir_favoritos),
            ("↩️  Sair",               self._sair),
        ]

        for i, (texto, cmd) in enumerate(itens):
            btn = ctk.CTkButton(
                popup, text=texto,
                height=46, corner_radius=0,
                fg_color="transparent",
                hover_color=SURFACE,
                font=ctk.CTkFont("Arial", 13),
                text_color=TEXT, anchor="w",
                command=lambda c=cmd: self._executar_opcao(c),
            )
            btn.pack(fill="x", padx=4, pady=(4 if i == 0 else 0, 0))

            if i < len(itens) - 1:
                ctk.CTkFrame(popup, height=1, fg_color=DIVIDER).pack(fill="x", padx=12)

    def _fechar_dropdown(self):
        if self._dropdown_win is not None:
            try:
                self._dropdown_win.destroy()
            except Exception:
                pass
            self._dropdown_win = None
        self.btn_perfil.configure(text="👤  Perfil  ▾")
        try:
            self.janela.unbind("<Button-1>")
        except Exception:
            pass

    def _fechar_se_fora(self, event):
        if self._dropdown_win is None:
            return
        try:
            px = self._dropdown_win.winfo_rootx()
            py = self._dropdown_win.winfo_rooty()
            pw = self._dropdown_win.winfo_width()
            ph = self._dropdown_win.winfo_height()
            if px <= event.x_root <= px + pw and py <= event.y_root <= py + ph:
                return
        except Exception:
            pass
        self._fechar_dropdown()

    def _executar_opcao(self, cmd):
        self._fechar_dropdown()
        cmd()

    # ── Ações do dropdown ─────────────────────────────────────────────────────

    def _ir_perfil(self):
        if self._janela_ja_aberta("perfil"):
            return
        from screens.profile_screen import ProfileWind
        instancia = ProfileWind(self.janela, self.usuario)
        self._open_windows["perfil"] = instancia

    def _ir_favoritos(self):
        from screens.favorite_screen import FavoritesWind
        FavoritesWind(self.janela,self.usuario)

    def _sair(self):
        self.video_running = False
        if self.video_capture:
            self.video_capture.release()
        self.janela.destroy()
        from screens.login_screen import LoginWind
        LoginWind()

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

    # ── Lógica de busca ───────────────────────────────────────────────────────

    def consult_push(self):
        search = self.buscarEntry.get().strip()
        if not search:
            messagebox.showwarning("Atenção", "Digite algo para pesquisar.")
            return
        self.buscarbotao.configure(state="disabled")
        self.janela.update()
        try:
            service = GoogleBookApi()
            results = service.consult_list(search)
            self.livros_resultados = results
            self.show_results(results)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na busca: {e}")
        finally:
            self.buscarbotao.configure(state="normal")

    def show_results(self, livros):
        for w in self.results_frame.winfo_children():
            w.destroy()

        if not livros:
            ctk.CTkLabel(
                self.results_frame,
                text="Nenhum livro encontrado.", text_color=MUTED,
                font=ctk.CTkFont("Arial", 14),
            ).pack(pady=40)
            return

        ctk.CTkLabel(
            self.results_frame,
            text=f"{len(livros)} resultado(s) encontrado(s)",
            font=ctk.CTkFont("Arial", 12), text_color=MUTED, anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 4))

        for livro in livros:
            self._book_card(livro)

    def _book_card(self, livro):
        card = ctk.CTkFrame(
            self.results_frame, fg_color=SURFACE,
            corner_radius=12,
        )
        card.pack(fill="x", padx=8, pady=6)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, padx=16, pady=14)

        ctk.CTkLabel(
            info, text=livro.get("Título", "—"),
            font=ctk.CTkFont("Georgia", 15, "bold"),
            text_color=PURPLE_LIGHT, anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            info, text=livro.get("Autor", "—"),
            font=ctk.CTkFont("Arial", 12), text_color=MUTED, anchor="w",
        ).pack(fill="x")

        meta = ctk.CTkFrame(info, fg_color="transparent")
        meta.pack(fill="x", pady=(6, 0))

        for label, key in [("💲", "Preço"), ("⭐", "Nota"), ("🌐", "Idioma")]:
            val = str(livro.get(key, "—"))
            if key == "Idioma":
                val = val.upper()
            ctk.CTkLabel(
                meta, text=f"{label} {val}",
                font=ctk.CTkFont("Arial", 11), text_color=MUTED,
            ).pack(side="left", padx=(0, 18))

        ctk.CTkButton(
            card, text="Ver detalhes →",
            width=130, height=36, corner_radius=8,
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont("Arial", 12, "bold"),
            command=lambda id_livro=livro["ID"]: self.open_details(id_livro),
        ).pack(side="right", padx=16, pady=14)

    def open_details(self, id_livro):
        if self._janela_ja_aberta(id_livro):
            return
        api = GoogleBookApi()
        details = api.consult_id(id_livro)
        from screens.book_details_screen import BookDetails
        instancia = BookDetails(self.janela, details, self.usuario)
        self._open_windows[id_livro] = instancia


if __name__ == "__main__":
    HomeWind()