import requests
from dotenv import load_dotenv
from tkinter import messagebox
import os

load_dotenv()

class GoogleBookApi:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_BOOKS_API")
        self.url = "https://www.googleapis.com/books/v1/volumes"

    def book_consult(self,livro):
        parameters = {
            "q" : livro,
            "key" : self.api_key
        }

        resposta = requests.get(self.url, params=parameters)

        if resposta.status_code == 465:
            messagebox.showerror("Erro","Erro na Chave API")
        
        if resposta.status_code == 400:
            messagebox.showerror("Erro","Campo de Pesquisa Vazio")
    
        return resposta.json()
    
    def consult_list(self, livro):
        dados = self.book_consult(livro)

        results = []

        for item in dados.get("items", []):
            infovolume = item.get("volumeInfo", {})
            infosale = item.get("saleInfo", {})
            infoprice = infosale.get("listPrice", {})
            imagens = infovolume.get("imageLinks", {})

            consulta = {
                "ID": item.get("id"),
                "Título": infovolume.get("title", "Sem título"),
                "Autor": infovolume.get("authors", ["Autor desconhecido"]),
                "Idioma": infovolume.get("language", "Indisponível"),
                "Nota": infovolume.get("averageRating", "Sem avaliação"),
                "Preço": f'{infoprice.get("amount", "Indisponível")} {infoprice.get("currencyCode", "")}',
                "Imagem": imagens.get("thumbnail", "Sem imagem")
            }

            results.append(consulta)

        return results
    
    def consult_id(self, book_id):
        url = f"{self.url}/{book_id}"

        parameters = {
            "key":  self.api_key
        }

        resposta = requests.get(url, params=parameters)
        item = resposta.json()

        infovolume = item.get("volumeInfo", {})
        infosale = item.get("saleInfo", {})
        infoprice = infosale.get("listPrice", {})
        imagens = infovolume.get("imageLinks", {})

        details = {
            "ID": item.get("id"),
            "Título": infovolume.get("title", "Sem título"),
            "Autor": infovolume.get("authors", ["Autor desconhecido"]),
            "Editora": infovolume.get("publisher", "Editora não informada"),
            "Descrição": infovolume.get("description", "Sem descrição"),
            "Num Páginas": infovolume.get("pageCount", "Quantidade indisponível"),
            "Idioma": infovolume.get("language", "Indisponível"),
            "Publicado": infovolume.get("publishedDate", "Data indisponível"),
            "Nota": infovolume.get("averageRating", "Sem avaliação"),
            "Preço": f'{infoprice.get("amount", "Indisponível")} {infoprice.get("currencyCode", "")}',
            "Link de Compra": infosale.get("buyLink", "Indisponível"),
            "Imagem": imagens.get("thumbnail", "Sem imagem")
        }

        return details



if __name__ == "__main__":    
    teste1 = GoogleBookApi()
    print(teste1.consult("Harry Potter"))
