from database.models import User
from database.models import Favorites

class UserRepository:
    def __init__(self, session):
        self.session = session

    
    def create_user(self, nome, email, senha):
        user = User(
            nome = nome,
            email = email,
            senha = senha
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
    
    def get_by_email(self, email):
        return (
            self.session
            .query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_id(self, user_id):
        return (
            self.session
            .query(User)
            .filter(User.id == user_id)
            .first()
        )
    
    def update_email(self, user_id, novo_email):
        user = self.get_by_id(user_id)

        if user is None:
            return False
        
        user.email = novo_email

        self.session.commit()
        self.session.refresh(user)

        return user
    
    def update_password(self, user_id, nova_senha):
        user = self.get_by_id(user_id)

        if user is None:
            return False

        user.senha = nova_senha

        self.session.commit()
        self.session.refresh(user)

        return user    
    
    

class FavoriteRepository:
    def __init__(self, session):
        self.session = session

    def add_favorite(self, user_id, livro):
        favorite = Favorites(
            user_id=user_id,
            book_id=livro.get("ID"),
            title=livro.get("Título"),
            autor=", ".join(livro.get("Autor", [])),
            descricao=livro.get("Descrição"),
            idioma=livro.get("Idioma"),
            preco=livro.get("Preço"),
            link_compra=livro.get("Link de Compra"),
            imagem=livro.get("Imagem"),
            editora=livro.get("Editora"),
            publicado=livro.get("Publicado"),
            num_paginas=livro.get("Num Páginas"),
            nota=livro.get("Nota")
        )

        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)

        return favorite
        
        
    def get_by_user_and_book(self, user_id, book_id):
        return (
            self.session
            .query(Favorites)
            .filter(
                Favorites.user_id == user_id,
                Favorites.book_id == book_id
            )
            .first()
        )

    def delete_favorite(self, user_id, book_id):
        favorite = self.get_by_user_and_book(user_id, book_id)

        if favorite is None:
            return False

        self.session.delete(favorite)
        self.session.commit()

        return True


    def get_user_fav(self, user_id):
        return (
            self.session
            .query(Favorites)
            .filter(Favorites.user_id == user_id)
            .all()
        )

    def is_favorite(self,user_id, book_id):
        favorite = self.get_by_user_and_book(user_id, book_id)

        return favorite is not None
