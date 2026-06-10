import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from services.google_books_service import GoogleBookApi


class HomeWind:
    def __init__(self):
        self.janela = tk.Tk()

        self.janela.title("LivrarIA Home")

        self.janela.geometry("1280x720")

        self.janela.resizable(False,False)

        self.perfilbotão = tk.Button(
            self.janela,
            text="Perfil",
            width=30,
            command=self.abrir_perfil
        )
        self.perfilbotão.pack(pady=20, padx=(10,1200))


        self.buscar = tk.Label(
            self.janela,
            text="Buscar Livros",
            font=("Arial",20)
        )
        self.buscar.pack()
        self.buscarEntry = tk.Entry(
            self.janela,
            width=90
        )
        self.buscarEntry.pack(pady=20)
        self.buscarbotao = tk.Button(
            self.janela,
            text="Procurar",
            width=30,
            font=("Arial",15),
            command=self.consult_push
        )
        self.buscarbotao.pack()
        
        self.paneltext = scrolledtext.ScrolledText(
            self.janela,
            font=("Arial",10),
            bg= "#ededed",
            width=150
        )
        self.paneltext.pack(pady=20)
        self.paneltext.config(state="disabled")

    def abrir_perfil(self):
        from screens.profile_screen import ProfileWind
        ProfileWind(self.janela)
    
    
    def buttom_sair(self):
        self.janela.destroy()
        from screens.login_screen import LoginWind
        LoginWind()
    
    def consult_push(self):
        search = self.buscarEntry.get()
        service = GoogleBookApi()
        results = service.consult_list(search)
        self.show_results(results)

    def show_results(self, livros):
        self.paneltext.config(state="normal")
        self.paneltext.delete("1.0","end")

        for info, livro in enumerate(livros):

            name_tag = f"livro_{info}"

            text = (
                f"Título:{livro["Título"]}\n"
                f"Autor:{livro["Autor"]}\n"
                f"Preço:{livro["Preço"]}\n"
                f"Capa:{livro["Imagem"]}\n"
                f"Nota:{livro["Nota"]}\n"
                f"Idioma:{livro["Idioma"].upper()}\n"
                f"{"." * 200}\n\n"
            )

            self.paneltext.insert("end",text,name_tag)

            self.paneltext.tag_config(name_tag, foreground="#8345b0", underline="False")

            self.paneltext.tag_bind(
                name_tag,
                "<Button-1>",
                lambda event, id_livro=livro["ID"]:self.open_details(id_livro)
            )
        
        self.paneltext.config(state="disabled")
    
    def open_details(self,id):
        from screens.book_details_screen import BookDetails
        api = GoogleBookApi()
        details = api.consult_id(id)

        BookDetails(self.janela,details)

if __name__ == "__main__":
    teste1 = HomeWind()
    teste1.janela.mainloop()