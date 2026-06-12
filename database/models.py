from sqlalchemy import Column, Integer, String
from database.connection import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(250), nullable=False)

    def to_dict(self):
        return{
            "id" : self.id,
            "nome" : self.nome,
            "email" : self.email,
        }

#class Favorites(Base):
#Ideia de acrescentar banco de favoritos para cada usuário

