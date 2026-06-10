import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import webbrowser
from services.google_books_service import GoogleBookApi

class BookDetails:
    def __init__(self, janela_home, details_book):
        self.janela_home = janela_home

        self.details_book = details_book

        self.janela = tk.Toplevel()

        self.janela.title(f"{details_book['Título']} Descrição")

        self.janela.geometry("600x800")

        self.janela.resizable(False,False)

        self.book_name = tk.Label(
            self.janela,
            text=f"{details_book['Título']}",
            font=("Times New Roman",20,"bold"),
            foreground="#8345b0"
        )
        self.book_name.pack(pady=10)

        self.author_name = tk.Label(
            self.janela,
            text=f"{details_book['Autor']}",
            font=("Arial", 10),
            foreground="#6C587A"
        )
        self.author_name.pack(pady=5)

        self.paneltext = scrolledtext.ScrolledText(
            self.janela,
            font=("Arial",10),
            bg= "#ededed",
            width=50
        )
        self.paneltext.pack(pady=10)
        self.paneltext.config(state="disabled")
        self.show_desc()

        self.savebutton = tk.Button(
            self.janela,
            text="Salvar Livro",
            width=30,
            command=None
        )
        self.savebutton.pack(pady=10)

        self.titleinfo = tk.Label(
            self.janela,
            text="Informações do Livro",
            font=("Times New Roman", 12, "bold"),
            foreground="#8345b0"
        )
        self.titleinfo.pack(pady=20)

        self.pagesquant = tk.Label( #Quantidade de páginas 
            self.janela,
            text=f"Páginas:   {details_book['Num Páginas']}",
            font=("Arial", 10),
            foreground="#6C587A"
        )
        self.pagesquant.pack(pady=5)
        

        self.publisher = tk.Label(  #Editora
            self.janela,
            text=f"Editora:   {details_book['Editora']}",
            font=("Arial", 10),
            foreground="#6C587A"
        )
        self.publisher.pack(pady=5)


        self.publishdate = tk.Label( #data de publicação
            self.janela,
            text=f"Publicado:   {details_book['Publicado']}",
            font=("Arial", 10),
            foreground="#6C587A"
        )
        self.publishdate.pack(pady=5)        


        self.ratingbook = tk.Label( #Nota
            self.janela,
            text=f"Nota:   {details_book['Nota']}",
            font=("Arial", 10),
            foreground="#6C587A"
        )
        self.ratingbook.pack(pady=5)

        self.buybutton = tk.Button(
            self.janela,
            text="Comprar Agora",
            width=30,
            command=self.link_buy,
            foreground="#8345b0"
        )
        self.buybutton.pack(pady=10)       



    def show_desc(self):
        self.paneltext.config(state="normal")
        self.paneltext.delete("1.0","end")

        description = self.details_book['Descrição']
        self.paneltext.insert("end",description)

        self.paneltext.config(state="disabled")
    
    def link_buy(self):
        url = self.details_book['Link de Compra']
        webbrowser.open(url)






