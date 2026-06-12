import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import connection,repository
import os
import cv2
import threading
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PURPLE      = "#6F18AD"
PURPLE_DARK = "#460574"

BG          = "#000214"  
BG_ALT      = "#05081A"  

SURFACE     = "#111B33"
TEXT        = "#E0D6F5"
MUTED       = "#9E8FAF"

ACCENT      = "#8B3DFF"
ACCENT_HOVER= "#A25CFF"

class LoginWind:
    def __init__(self):

        db = connection.DatabaseManager()
        db.create_tables()
        session = db.create_session()
        self.repository = repository.UserRepository(session)

        self.janela = ctk.CTk()
        self.janela.title("kadeMeuLivro — Login")
        self.janela.resizable(False, False)
        self.janela.configure(fg_color=BG)
        self.janela.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        self.video_running = True
        self.video_label = None
        self.video_capture = None

        self._build_ui()
        self._centralizar(420, 620)
        self.janela.mainloop()

    def _centralizar(self, largura, altura):
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth()  // 2) - (largura // 2)
        y = (self.janela.winfo_screenheight() // 2) - (altura  // 2)
        self.janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def _on_closing(self):
        """Para o vídeo e fecha a aplicação corretamente"""
        self.video_running = False
        if self.video_capture:
            self.video_capture.release()
        self.janela.destroy()

    def _play_video(self):
        """Toca o vídeo em loop"""
        while self.video_running:
            try:
                # Verificar se a janela ainda existe
                if not self.janela.winfo_exists():
                    break
                    
                ret, frame = self.video_capture.read()
                
                if not ret:
                    # Reiniciar o vídeo quando terminar
                    self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                # Redimensionar frame para 300x140
                frame = cv2.resize(frame, (300, 140))
                
                # Converter BGR para RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Converter para PIL Image
                image = Image.fromarray(frame)
                
                # Converter para PhotoImage
                photo = ImageTk.PhotoImage(image)
                
                # Atualizar label com novo frame
                if self.video_label and self.janela.winfo_exists():
                    self.video_label.configure(image=photo)
                    self.video_label.image = photo
                
                # Controlar FPS (30 FPS) - usar time.sleep em vez de after()
                time.sleep(0.033)
            except Exception:
                # Se houver erro (janela destruída, etc), sair da thread
                break
    
    def _build_ui(self):
        # ── Vídeo ────────────────────────────────────────────────────────────
        video_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "pixel cat.mp4")
        
        self.video_label = ctk.CTkLabel(
            self.janela,
            text="",
            fg_color=SURFACE,
        )
        self.video_label.pack(pady=(24, 0))
        
        # Iniciar vídeo em thread separada
        self.video_capture = cv2.VideoCapture(video_path)
        video_thread = threading.Thread(target=self._play_video, daemon=True)
        video_thread.start()

        # ── Card ─────────────────────────────────────────────────────────────
        card = ctk.CTkFrame(self.janela, fg_color=SURFACE, corner_radius=16)
        card.pack(padx=40, pady=(0, 0), fill="x")

        ctk.CTkLabel(card, text="E-mail", font=ctk.CTkFont("Arial", 12),
                     text_color=MUTED, anchor="w").pack(padx=24, pady=(20, 2), fill="x")
        self.emailentry = ctk.CTkEntry(
            card, placeholder_text="seu@email.com",
            height=40, corner_radius=8,
            fg_color="#0f0f23", border_color=PURPLE,
            text_color=TEXT, font=ctk.CTkFont("Arial", 13),
        )
        self.emailentry.pack(padx=24, fill="x")

        ctk.CTkLabel(card, text="Senha", font=ctk.CTkFont("Arial", 12),
                     text_color=MUTED, anchor="w").pack(padx=24, pady=(12, 2), fill="x")
        self.senhaentry = ctk.CTkEntry(
            card, placeholder_text="••••••••", show="•",
            height=40, corner_radius=8,
            fg_color="#0f0f23", border_color=PURPLE,
            text_color=TEXT, font=ctk.CTkFont("Arial", 13),
        )
        self.senhaentry.pack(padx=24, fill="x")
        self.senhaentry.bind("<Return>", lambda e: self.enviar())

        ctk.CTkButton(
            card, text="Esqueceu a senha?",
            font=ctk.CTkFont("Arial", 11), text_color=PURPLE,
            fg_color="transparent", hover=False, anchor="e",
            command=None,
        ).pack(padx=24, pady=(4, 0), fill="x")

        ctk.CTkButton(
            card, text="Entrar",
            height=44, corner_radius=10,
            fg_color=PURPLE, hover_color=PURPLE_DARK,
            font=ctk.CTkFont("Arial", 14, "bold"),
            text_color="white", command=self.enviar,
        ).pack(padx=24, pady=(12, 20), fill="x")

        # ── Rodapé ───────────────────────────────────────────────────────────
        footer = ctk.CTkFrame(self.janela, fg_color="transparent")
        footer.pack(pady=14)
        ctk.CTkLabel(footer, text="Não tem conta?",
                     text_color=MUTED, font=ctk.CTkFont("Arial", 12)).pack(side="left")
        ctk.CTkButton(
            footer, text=" Registrar",
            fg_color="transparent", hover=False,
            text_color=PURPLE, font=ctk.CTkFont("Arial", 12, "bold"),
            command=self.abrir_registrar,
        ).pack(side="left")

    def enviar(self):
        email = self.emailentry.get().strip()
        senha = self.senhaentry.get()
        usuario = self.repository.get_by_email(email)

        try:
            from screens.home_screen import HomeWind
            if usuario is None:
                messagebox.showerror("Erro", "Usuário não encontrado.")
                return
            if senha == usuario.senha:
                messagebox.showinfo("Sucesso", "Logado com sucesso!")
                self.janela.destroy()
                self.abrir_home(usuario)
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        except ValueError:
            messagebox.showerror("Erro", "Erro de valor inesperado.")

    def abrir_home(self,usuario):
        from screens.home_screen import HomeWind
        HomeWind(usuario)

    def abrir_registrar(self):
        self.janela.destroy()
        from screens.register_screen import RegisterWind
        RegisterWind()


if __name__ == "__main__":
    LoginWind()