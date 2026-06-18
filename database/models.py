from sqlalchemy import Column, Integer, String, ForeignKey,Text
from sqlalchemy.orm import relationship
from database.connection import Base
from services.google_books_service import GoogleBookApi


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(250), nullable=False)

    livros = relationship(
        "Favorites", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    

    def to_dict(self):
        return{
            "id" : self.id,
            "nome" : self.nome,
            "email" : self.email,
        }

class Favorites(Base):

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)


    book_id = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    autor =  Column(String(300), nullable=False)
    descricao = Column(Text, nullable=True)
    idioma = Column(String(50), nullable=True)
    preco = Column(String(100), nullable=True)
    link_compra = Column(Text, nullable=True)
    imagem = Column(Text, nullable=True)
    editora = Column(String(200), nullable=True)
    publicado = Column(String(30), nullable=True)
    num_paginas = Column(Integer, nullable=True)
    nota = Column(String(20), nullable=True)

    user = relationship(
        "User",
        back_populates="livros"
    )
    
    def to_dict(self):
        return{
        "id": self.id,
        "user_id": self.user_id,
        "book_id": self.book_id,
        "title": self.title,
        "autor": self.autor,
        "descricao": self.descricao,
        "idioma": self.idioma,
        "preco": self.preco,
        "link_compra": self.link_compra,
        "imagem": self.imagem,
        "editora": self.editora,
        "publicado": self.publicado,
        "num_paginas": self.num_paginas,
        "nota": self.nota
        }


