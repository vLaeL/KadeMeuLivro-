from database.models import User

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
    
    def update_username(self, user_id, novo_nome):
         user = self.get_by_id(user_id)

         if user is None:
             return False
         user.nome = novo_nome

         self.session.commit()
         self.session.refresh(user)

         return user
    
    def delete_by_id(self, user_id):
        user = self.get_by_id(user_id)

        if user is None:
            return False
        
        self.session.delete(user)
        self.session.commit()

        return True